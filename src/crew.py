import os
import sys
import time
import requests
from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew, Process
from crewai.tools import tool
from ddgs import DDGS

# Force UTF-8 output to avoid charmap errors on Windows
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)

load_dotenv()

@tool("Search Jobs")
def search_jobs(query: str) -> str:
    """
    Search for job postings using Adzuna API with a fallback to DuckDuckGo Search.
    
    Args:
        query: The job title or keywords to search for.
    """
    adzuna_app_id = os.environ.get("ADZUNA_APP_ID")
    adzuna_app_key = os.environ.get("ADZUNA_APP_KEY")
    
    # Attempt to use Adzuna API if credentials are present
    if adzuna_app_id and adzuna_app_key:
        try:
            # API endpoint for UK/GB region, page 1
            url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
            params = {
                "app_id": adzuna_app_id,
                "app_key": adzuna_app_key,
                "results_per_page": 8,
                "what": query
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for job in data.get("results", []):
                title = job.get("title", "N/A")
                company = job.get("company", {}).get("display_name", "N/A")
                location = job.get("location", {}).get("display_name", "N/A")
                salary_min = job.get("salary_min")
                salary_max = job.get("salary_max")
                
                if salary_min and salary_max:
                    salary = f"£{salary_min} - £{salary_max}"
                elif salary_min:
                    salary = f"£{salary_min}"
                else:
                    salary = "N/A"
                    
                description = job.get("description", "N/A")
                job_url = job.get("redirect_url", "N/A")
                
                results.append(
                    f"TITLE: {title}\n"
                    f"COMPANY: {company}\n"
                    f"LOCATION: {location}\n"
                    f"SALARY: {salary}\n"
                    f"DESCRIPTION: {description}\n"
                    f"URL: {job_url}"
                )
            
            if results:
                return "\n\n---\n\n".join(results)
                
        except Exception as e:
            print(f"Adzuna API failed: {e}. Falling back to DuckDuckGo Search...")

    # Fallback to DuckDuckGo Search
    print("Using DuckDuckGo Search fallback...")
    search_query = f"{query} site:linkedin.com/jobs OR site:indeed.com OR site:glassdoor.com"
    
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                # Use duckduckgo to fetch up to 8 results
                results = list(ddgs.text(search_query, max_results=8))
                
                formatted_results = []
                for res in results:
                    title = res.get("title", "N/A")
                    body = res.get("body", "N/A")
                    href = res.get("href", "N/A")
                    
                    # Company, Location, and Salary are not easily extracted from generic search snippets
                    formatted_results.append(
                        f"TITLE: {title}\n"
                        f"COMPANY: N/A (See description or URL)\n"
                        f"LOCATION: N/A\n"
                        f"SALARY: N/A\n"
                        f"DESCRIPTION: {body}\n"
                        f"URL: {href}"
                    )
                
                if formatted_results:
                    return "\n\n---\n\n".join(formatted_results)
                return "No jobs found via fallback search."
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2)  # Wait for 2 seconds before retrying
                
    return "Job search failed after 3 attempts."

@tool("Search Courses")
def search_courses(skill: str) -> str:
    """
    Search for free courses using DuckDuckGo Search.
    
    Args:
        skill: The skill to search for courses on.
    """
    print(f"Searching for free courses on {skill}...")
    search_query = f"free course learn {skill} 2024 site:coursera.org OR site:edx.org OR site:freecodecamp.org OR site:youtube.com"
    
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(search_query, max_results=5))
                
                formatted_results = []
                for res in results:
                    title = res.get("title", "N/A")
                    body = res.get("body", "N/A")
                    href = res.get("href", "N/A")
                    
                    formatted_results.append(
                        f"TITLE: {title}\n"
                        f"DESCRIPTION: {body}\n"
                        f"URL: {href}"
                    )
                
                if formatted_results:
                    return "\n\n---\n\n".join(formatted_results)
                return "No courses found."
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2)
                
    return "Course search failed after 3 attempts."

@tool("Search Salary Data")
def search_salary_data(query: str) -> str:
    """
    Search for salary data using DuckDuckGo Search.
    
    Args:
        query: The job title or role to search salary data for.
    """
    print(f"Searching for salary data for {query}...")
    search_query = f"{query} average salary 2024 site:glassdoor.com OR site:levels.fyi OR site:payscale.com"
    
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(search_query, max_results=5))
                
                formatted_results = []
                for res in results:
                    title = res.get("title", "N/A")
                    body = res.get("body", "N/A")
                    href = res.get("href", "N/A")
                    
                    formatted_results.append(
                        f"TITLE: {title}\n"
                        f"SNIPPET: {body}\n"
                        f"URL: {href}"
                    )
                
                if formatted_results:
                    return "\n\n---\n\n".join(formatted_results)
                return "No salary data found."
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(2)
                
    return "Salary search failed after 3 attempts."

def get_llm(provider: str) -> LLM:
    """
    Get the appropriate LLM based on the provider string.
    """
    provider_lower = provider.lower()
    if 'gemini' in provider_lower:
        return LLM(model="gemini/gemini-1.5-flash")
    elif 'groq' in provider_lower:
        return LLM(model="groq/llama-3.3-70b-versatile")
    elif 'claude' in provider_lower:
        return LLM(model="anthropic/claude-3-5-haiku-20241022")
    else:
        return LLM(model="gpt-4o-mini")

def supports_tools(provider: str) -> bool:
    """
    Check if the selected provider reliably supports tool use.
    """
    return 'groq' not in provider.lower()

def safe_output(task: Task) -> str:
    """Safely extract string content from a Task object."""
    if task.output and hasattr(task.output, 'raw'):
        return task.output.raw
    return str(task.output) if task.output else ""

def run_career_intelligence(profile: str, interests: str, provider: str) -> dict:
    """Run the Career Intelligence Agent workflow."""
    llm = get_llm(provider)
    use_tools = supports_tools(provider)
    
    # Define Agents
    scout_agent = Agent(
        role="Career Scout",
        goal="Find relevant job postings based on user interests.",
        backstory="An expert career scout who finds the best job opportunities.",
        llm=llm,
        tools=[search_jobs] if use_tools else []
    )
    
    matcher_agent = Agent(
        role="Profile Matcher",
        goal="Match user profile to job requirements.",
        backstory="An expert HR recruiter who matches candidates to jobs.",
        llm=llm
    )
    
    gap_agent = Agent(
        role="Skills Gap Analyst",
        goal="Identify skills gap and provide salary data.",
        backstory="An analyst who identifies what skills a candidate is missing and researches salary expectations.",
        llm=llm,
        tools=[search_salary_data] if use_tools else []
    )
    
    roadmap_agent = Agent(
        role="Career Roadmap Planner",
        goal="Create an 8-week learning roadmap based on skills gaps.",
        backstory="A career coach who creates actionable learning plans.",
        llm=llm,
        tools=[search_courses] if use_tools else []
    )
    
    # Define Tasks
    scout_task = Task(
        description=f"Search for jobs based on the following interests: {interests}",
        expected_output="A list of job postings with title, company, location, salary, description, and URL.",
        agent=scout_agent
    )
    
    match_task = Task(
        description=f"Use the profile '{profile}' and the scout's context to list required skills and mark them ✅/🔶/❌ with a match percentage.",
        expected_output="A list of required skills marked ✅ (expert), 🔶 (intermediate), or ❌ (missing) with an overall match percentage.",
        agent=matcher_agent,
        context=[scout_task]
    )
    
    gap_task = Task(
        description="Create a priority ranking of missing skills and search for salary data based on the matcher's context.",
        expected_output="A prioritized list of missing skills and average salary data.",
        agent=gap_agent,
        context=[match_task]
    )
    
    roadmap_task = Task(
        description="Generate a week-by-week 8-week roadmap specifying courses, projects, and unlocks based on the gap context.",
        expected_output="A week-by-week 8-week roadmap with recommended courses, projects, and career unlocks.",
        agent=roadmap_agent,
        context=[gap_task]
    )
    
    # Initialize Crew
    crew = Crew(
        agents=[scout_agent, matcher_agent, gap_agent, roadmap_agent],
        tasks=[scout_task, match_task, gap_task, roadmap_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Kickoff
    crew.kickoff()
    
    return {
        "jobs": safe_output(scout_task),
        "matching": safe_output(match_task),
        "gaps": safe_output(gap_task),
        "roadmap": safe_output(roadmap_task)
    }
