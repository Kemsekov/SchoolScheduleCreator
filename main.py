import json
from typing import Dict
import networkx as nx
data = json.load(open('data.json'))
#empty lesson
filler="---"


# a list of lessons
lessons = data["lessons"]

# a limit to how much repetition of the same lesson per day is allowed
same_lessons_repeats_per_day_per_group_limit = int(data["same_lessons_repeats_per_day_per_group_limit"])


# a list of groups data :
# group name and count of lessons this group need to fill in each 
# week. Like group A need to fill 4 math and physics lessons per week and just two lessons
# of other disciplines.
groups_plans = data["groups_plans"]
# a limit to how much lessons per for student day allowed 
group_lessons_per_day_limit = {
        g['name']:g['lessons_limit'] for g in groups_plans
    }
week = data["studying_period"]

teacher_lessons_limits = {
        # key is lesson at particular day, a limit is how much lesson's teacher can handle per day
        day+'_'+l['name']:int(l["lessons_limit"])
        for l in lessons for day in week
    }

def init_group(group):
    graph = nx.DiGraph()
    name = group["name"]
    end = "end"
    graph.add_node(name)
    graph.add_node(end)

    for day in week:
        graph.add_node(day)
        graph.add_edge(name,day,capacity=group_lessons_per_day_limit[name])

    for l in lessons:
        l=l['name']
        lessons_limit = int(group[l])
        graph.add_node(l)
        graph.add_edge(l,end,capacity=lessons_limit)
    
    for day in week:
        for l in lessons:
            l=l['name']
            day_lesson = day+'_'+l
            graph.add_node(day_lesson)
            graph.add_edge(day,day_lesson,capacity=same_lessons_repeats_per_day_per_group_limit)
            capacity = teacher_lessons_limits[day_lesson]
            graph.add_edge(day_lesson,l,capacity=capacity)
    return graph

def solve_group_graph(group_name : str,end_point_name : str,graph : nx.Graph):
    flow_value, flow_dict = nx.maximum_flow(graph,group_name,end_point_name)
    for day in week:
        for l in lessons:
            l=l['name']
            day_lesson = day+'_'+l
            teacher_lessons_limits[day_lesson]-=flow_dict[day_lesson][l]
    return flow_value, flow_dict

def count_group_expected_lessons_in_week(group):
    result = 0
    for l in lessons:
        l=l['name']
        result+=int(group[l])
    return result

def print_limits():
    [print(f'{i} {teacher_lessons_limits[i]}') for i in teacher_lessons_limits]
    print("----------------")

def create_schedule(flow_dict : dict):
    result = {}
    for day in week:
        result[day] = []
        for l in lessons:
            l=l['name']
            day_lesson = day+'_'+l
            lessons_count = flow_dict[day][day_lesson]
            for n in range(lessons_count):
                result[day].append(l)
        pass
    return result

def print_schedule(group_name : str, schedule : dict):
    print(f"Group {group_name}\n")
    for i in schedule:
        print(f"{i}:")
        for lesson in schedule[i]:
            print(f"\t{lesson}")
        print()
    print('-----------------')

def ensure_list_have_size_at_least(l : list, size : int, fill_element):
    while len(l)<=size:
        l.append(fill_element)

# there is cases when same discipline must be held in different
# groups at the same time. We assume teacher cannot be in two places
# simultaneously so we need to reorder each day schedule a bit
# by changing order in which disciplines held for each group                   

def reorder_schedules(schedules : list[Dict[str,list[str]]],group_names : list[str]):
    for day in week:
        graph = nx.MultiGraph()

        name_to_schedule = {}
        index = 0
        for group_schedule in schedules:
            name=group_names[index]
            day_schedule = group_schedule[day]
            name_to_schedule[name]=day_schedule
            graph.add_node(name)
            index+=1
            for lesson in day_schedule:
                graph.add_edge(name,lesson,name=name,lesson=lesson) 
            day_schedule.clear()
        
        lesson_index=0
        line_graph=nx.line_graph(graph)

        edge_lesson=nx.get_edge_attributes(graph,"lesson")
        edge_group_name=nx.get_edge_attributes(graph,"name")

        while True:
            if(len(line_graph.nodes)==0): break
            independent_set =  nx.maximal_independent_set(line_graph)
            for node in independent_set:
                lesson=edge_lesson[node]
                group_name=edge_group_name[node]
                schedule=name_to_schedule[group_name]
                ensure_list_have_size_at_least(schedule,lesson_index,filler)
                schedule[lesson_index]=lesson
                line_graph.remove_node(node)
            lesson_index+=1


#at the end we check that schedules are fitting all necessary requirements
def check_schedules(schedules : list[Dict[str,list[str]]],group_names : list[str]):
    index = 0
    for schedule in schedules:
        name = group_names[index]
        max_lessons = group_lessons_per_day_limit[name]
        required_plan = groups_plans[index]
        complete_lessons = {lesson["name"]:required_plan[lesson["name"]] for lesson in lessons}
        for day in week:
            day_schedule = schedule[day]
            lessons_count=0
            for lesson in day_schedule:
                if lesson != filler:
                    complete_lessons[lesson]-=1
                    lessons_count+=1
            if lessons_count>max_lessons:
                raise Exception("Exceed max lessons count on "+day+" for group "+name)
        for plan in complete_lessons:
            if complete_lessons[plan]!=0:
                raise Exception("Schedule does not completes plan for group "+name+"\n Missing "+complete_lessons[plan]+" on lesson "+plan)
        index+=1
    for day in week:
        index = 0
        lessons_count_on_day = {lesson["name"]:0 for lesson in lessons}
        lessons_intersection : Dict[int,list[str]]= {}
        for schedule in schedules:
            name = group_names[index]
            same_lessons_count = {lesson["name"]:0 for lesson in lessons}
            lesson_id = 0
            for lesson in schedule[day]:
                if lesson != filler:
                    if lesson_id not in lessons_intersection:
                        lessons_intersection[lesson_id]=list()
                    lessons_intersection[lesson_id].append(lesson)
                    lessons_count_on_day[lesson]+=1
                    same_lessons_count[lesson]+=1
                lesson_id+=1
           
            for lesson in same_lessons_count:
                if same_lessons_count[lesson]>same_lessons_repeats_per_day_per_group_limit:
                    raise Exception("On day "+day+" on group "+name+" count of "+lesson+" lessons exceed max lessons repeats per day for group")
            index+=1
        
        for id in lessons_intersection:
            lessons_on_same_id=lessons_intersection[id]
            if len(set(lessons_on_same_id))!=len(lessons_on_same_id):
                raise Exception("On day "+day+" there is same lessons intersection among groups : "+str(lessons_on_same_id))
        for lesson in lessons:
            if lessons_count_on_day[lesson['name']]>lesson["lessons_limit"]:
                raise Exception("On day "+day+" on lesson "+lesson['name']+" lessons count exceed maximum lessons restrain")


def main():
    schedules = []
    group_names : list[str] = []
    for g in groups_plans:
        group_name = g["name"]
        graph = init_group(g)
        expected_lessons = count_group_expected_lessons_in_week(g)
        lessons_count,max_flow = solve_group_graph(group_name,"end",graph)
        if(expected_lessons!=lessons_count):
            print("Expected lessons count not equal builded by schedules lessons count")
            print(f'{expected_lessons}!={lessons_count}')
            print("Impossible to create a schedule for group "+group_name)
            print("Try decrease lessons count for this group or increase same_lessons_repeats_per_day_per_group_limit")
            return
        schedule = create_schedule(max_flow)
        schedules.append(schedule)
        group_names.append(group_name)
    
    reorder_schedules(schedules,group_names)
    check_schedules(schedules,group_names)
    for group_name,schedule in zip(group_names,schedules):
        print_schedule(group_name,schedule)

if __name__ == "__main__":
    main()