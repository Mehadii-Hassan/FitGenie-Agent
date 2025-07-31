import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

# --- Load environment variables ---
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set BASE_URL, API_KEY, and MODEL_NAME.")

# --- OpenAI Client Setup ---
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# --- Dummy Data ---
WORKOUT_PLANS = {
    "weight loss": ["HIIT", "Cardio", "Circuit Training"],
    "muscle gain": ["Strength Training", "Compound Lifts", "Split Routines"],
    "flexibility": ["Yoga", "Dynamic Stretching", "Pilates"]
}

NUTRITION_GUIDES = {
    "weight loss": ["Low Carb Diet", "Intermittent Fasting", "Calorie Deficit"],
    "muscle gain": ["High Protein Meal Plan", "Creatine Guide", "Bulking Diet Tips"],
    "flexibility": ["Hydration Tips", "Anti-inflammatory Foods", "Balanced Macronutrients"]
}

COURSES = {
    "HIIT": ["30-Day HIIT Challenge (FitOn) - https://example.com/hiit"],
    "Strength Training": ["Strength Training Basics (Udemy) - https://example.com/strength"],
    "Yoga": ["Yoga for Beginners (YouTube) - https://example.com/yoga"],
}

# --- Models ---
class FitnessGap(BaseModel):
    fitness_goal: str
    missing_workouts: List[str]
    explanation: str

class NutritionAdvice(BaseModel):
    goal: str
    tips: List[str]

class WorkoutCourseRecommendation(BaseModel):
    workout: str
    courses: List[str]

# --- Tools ---
@function_tool
def get_fitness_gaps(current_routine: List[str], fitness_goal: str) -> dict:
    required = WORKOUT_PLANS.get(fitness_goal.lower())
    if not required:
        return {"error": f"No data for goal: {fitness_goal}"}
    missing = [plan for plan in required if plan not in current_routine]
    return {
        "fitness_goal": fitness_goal,
        "missing_workouts": missing,
        "explanation": f"To achieve '{fitness_goal}', consider adding: {', '.join(missing)}"
    }

@function_tool
def suggest_nutrition(fitness_goal: str) -> List[str]:
    return NUTRITION_GUIDES.get(fitness_goal.lower(), [])

@function_tool
def recommend_fitness_courses(missing_workouts: List[str]) -> List[dict]:
    recommendations = []
    for workout in missing_workouts:
        courses = COURSES.get(workout)
        if courses:
            recommendations.append({
                "workout": workout,
                "courses": courses
            })
    return recommendations

# --- Specialist Agents ---
fitness_gap_agent = Agent(
    name="Fitness Gap Specialist",
    handoff_description="Identifies missing workouts for a fitness goal.",
    instructions="""
    Use get_fitness_gaps tool to compare user's routine with required workouts.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[get_fitness_gaps],
    output_type=FitnessGap
)

nutrition_guide_agent = Agent(
    name="Nutrition Advisor",
    handoff_description="Suggests diets based on user's goal.",
    instructions="""
    Use suggest_nutrition tool to suggest relevant dietary advice.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[suggest_nutrition],
    output_type=List[str]
)

fitness_course_agent = Agent(
    name="Fitness Course Recommender",
    handoff_description="Finds learning resources for workouts.",
    instructions="""
    Use recommend_fitness_courses tool to suggest workout guidance.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[recommend_fitness_courses],
    output_type=List[WorkoutCourseRecommendation]
)

# --- Main Controller Agent ---
fitgenie_agent = Agent(
    name="FitGenie",
    instructions="""
    You are the user's personal fitness planner.
    - Ask about their goal (e.g., weight loss).
    - If they mention missing workouts or routines, use Fitness Gap Specialist.
    - If they want food guidance, send to Nutrition Advisor.
    - If they want workout tutorials, send to Fitness Course Recommender.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    handoffs=[fitness_gap_agent, nutrition_guide_agent, fitness_course_agent]
)

# --- Main Function ---
async def main():
    queries = [
        "I want to lose weight",
        "I only do Cardio. What's missing?",
        "Suggest a good workout course for HIIT",
        "What should I eat to gain muscle?"
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        result = await Runner.run(fitgenie_agent, query)
        output = result.final_output

        print("\nFINAL RESPONSE:")

        if isinstance(output, FitnessGap):
            print("\n🏋️ FITNESS GAP")
            print(f"Goal: {output.fitness_goal}")
            print(f"Missing Workouts: {', '.join(output.missing_workouts)}")
            print(f"Advice: {output.explanation}")

        elif isinstance(output, list) and all(isinstance(tip, str) for tip in output):
            print("\n🥗 NUTRITION TIPS")
            for i, tip in enumerate(output, 1):
                print(f"{i}. {tip}")

        elif isinstance(output, list) and all(isinstance(rec, WorkoutCourseRecommendation) for rec in output):
            print("\n📚 WORKOUT COURSES")
            for rec in output:
                print(f"\nWorkout: {rec.workout}")
                for i, course in enumerate(rec.courses, 1):
                    print(f"  {i}. {course}")

        else:
            print(output)

if __name__ == "__main__":
    asyncio.run(main())
