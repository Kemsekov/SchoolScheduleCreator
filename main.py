import json
from typing import Dict
import networkx as nx
data = json.load(open('data.json'))
# a list of lessons
lessons = data["lessons"]
# a limit to how much lessons per for student day allowed 
student_lessons_per_day_limit = int(data["student_lessons_per_day_limit"])
# a limit to how much repetition of the same lesson per day is allowed
same_lessons_repeats_per_day_per_group_limit = int(data["same_lessons_repeats_per_day_per_group_limit"])
# a limit to how much lessons teacher can handle per day
teacher_lessons_per_day_limit = int(data["teacher_lessons_per_day_limit"])

# a list of groups data :
# group name and count of lessons this group need to fill in each 
# week. Like group A need to fill 4 math and physics lessons per week and just two lessons
# of other disciplines.
groups_plans = data["groups_plans"]

week = ["monday","tuesday","wednesday","thursday","friday"]

teacher_lessons_limits = {
        day+'_'+l:teacher_lessons_per_day_limit
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
        graph.add_edge(name,day,capacity=student_lessons_per_day_limit)

    for l in lessons:
        lessons_limit = int(group[l])
        graph.add_node(l)
        graph.add_edge(l,end,capacity=lessons_limit)
    
    for day in week:
        for l in lessons:
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
            day_lesson = day+'_'+l
            teacher_lessons_limits[day_lesson]-=flow_dict[day_lesson][l]
    return flow_value, flow_dict

def count_group_expected_lessons_in_week(group):
    result = 0
    for l in lessons:
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
        graph = nx.DiGraph()
        end="end"
        start="start"
        graph.add_node(end)
        graph.add_node(start)
        for lesson in lessons:
            for id in range(0,student_lessons_per_day_limit):
                lesson_id=lesson+'_'+str(id)
                graph.add_node(lesson_id)
                graph.add_edge(lesson_id,end,capacity=1)

        index = 0
        for group_schedule in schedules:
            name=group_names[index]
            day_schedule = group_schedule[day]
            graph.add_node(name)
            graph.add_edge(start,name)
            index+=1
            for lesson in set(day_schedule):
                required_lesson=name+'_'+lesson
                graph.add_node(required_lesson)
                graph.add_edge(name,required_lesson,capacity=day_schedule.count(lesson))
                for id in range(0,student_lessons_per_day_limit):
                    graph.add_edge(required_lesson,lesson+'_'+str(id), capacity=1)
        # now we need to find max flow trough this graph, where each
        # group is source, and end is sink. 
        # We need edge between group name and required lesson to be filled with 1!
        flow_value, flow_dict = nx.maximum_flow(graph,start,end)
        for edge in graph.edges:
            print(edge)
            print(flow_dict[edge[0]][edge[1]])
            print("----------")
        index = 0
        fill_element="---"
        for group_schedule in schedules:
            name=group_names[index]
            day_schedule = group_schedule[day]
            index+=1
            for edge in graph.edges(name):
                if flow_dict[edge[0]][edge[1]]!=1:
                    print("Count not fit all required lessons!")
                    return
            day_schedule_copy = day_schedule.copy()
            day_schedule.clear()
            for lesson in set(day_schedule_copy):
                required_lesson=name+'_'+lesson
                def assign_lesson():
                    for id in range(0,student_lessons_per_day_limit):
                        lesson_id=lesson+'_'+str(id)
                        if flow_dict[required_lesson][lesson_id]==1:
                            ensure_list_have_size_at_least(day_schedule,id,fill_element)
                            day_schedule[id] = lesson
                            return True
                    return False
                if not assign_lesson():
                    print("Count not fit all required lessons!")
                    return
            

def main():
    schedules = []
    group_names : list[str] = []
    for g in groups_plans:
        group_name = g["name"]
        graph = init_group(g)
        expected_lessons = count_group_expected_lessons_in_week(g)
        lessons_count,max_flow = solve_group_graph(group_name,"end",graph)
        if(expected_lessons!=lessons_count):
            print(f'{expected_lessons}!={lessons_count}')
            print("Impossible to create a schedule with given input")
            return
        schedule = create_schedule(max_flow)
        schedules.append(schedule)
        group_names.append(group_name)
    reorder_schedules(schedules,group_names)
    for group_name,schedule in zip(group_names,schedules):
        print_schedule(group_name,schedule)
    pass

if __name__ == "__main__":
    main()