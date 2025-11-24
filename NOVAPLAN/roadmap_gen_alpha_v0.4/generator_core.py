import random
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class RoadmapStep:
    title: str
    objective: str
    duration_months: int
    prerequisites: List[str]
    milestones: List[str]
    resources: List[str]
    tasks: List[str] = field(default_factory=list)
    children: List['RoadmapStep'] = field(default_factory=list)

@dataclass
class Roadmap:
    path_title: str
    focus: str
    confidence_score: float
    steps: List[RoadmapStep]


def generate_steps_for_career(career: Dict[str,Any], profile_skills: List[str], focus: str, beginner: bool = True):
    known = [s for s in [sk.lower() for sk in career.get('skills', [])] if s in profile_skills]
    missing = [s for s in [sk.lower() for sk in career.get('skills', [])] if s not in profile_skills]

    def make_step(title, objective, months, prereq, milestones, resources, tasks=None, children=None):
        return RoadmapStep(
            title=title,
            objective=objective,
            duration_months=months,
            prerequisites=prereq,
            milestones=milestones,
            resources=resources,
            tasks=tasks or [],
            children=children or []
        )

    # Enhanced sections with detailed tasks and guidance
    career_tasks = career.get('tasks', [])
    career_name = career.get('career', 'Career')
    
    foundations_children = []
    if beginner:
        foundations_children = [
            make_step(
                'Computer Basics', 
                'Master essential computer skills for your career', 
                1, 
                [], 
                ['Complete command-line tutorial', 'Set up development environment', 'Create first project folder'],
                ['Codecademy CLI Course', 'VS Code Documentation', 'GitHub Desktop'],
                [
                    'Install VS Code and configure extensions',
                    'Learn basic terminal commands (cd, ls, mkdir, touch)',
                    'Create a project folder structure',
                    'Set up version control with Git',
                    'Complete Codecademy CLI course'
                ]
            ),
            make_step(
                'Math & Logic Basics', 
                'Build analytical thinking foundation', 
                1, 
                [], 
                ['Complete Khan Academy modules', 'Solve 20 practice problems', 'Understand basic statistics'],
                ['Khan Academy', 'Coursera Logic Course', 'Brilliant.org'],
                [
                    'Complete Khan Academy Algebra basics',
                    'Practice logical reasoning problems',
                    'Learn basic statistics concepts',
                    'Complete 20 problem-solving exercises',
                    'Take a logic fundamentals course'
                ]
            ),
        ]
    foundations = make_step(
        'Foundations', 
        'Build essential groundwork for your career', 
        1 if beginner else 0, 
        [], 
        ['Complete all foundation modules', 'Set up workspace', 'Create learning schedule'],
        ['VS Code', 'Git', 'Notion/Trello', 'Calendar app'],
        [
            'Set up your learning workspace',
            'Create a study schedule',
            'Install all necessary tools',
            'Join relevant online communities',
            'Set up project tracking system'
        ],
        children=foundations_children
    )

    core_children = []
    for i, sk in enumerate((missing[:4] or career.get('skills', [])[:4])):
        skill_tasks = []
        if career_tasks:
            # Extract relevant tasks for this skill
            skill_tasks = [task for task in career_tasks[:3] if sk.lower() in task.lower()][:3]
        
        if not skill_tasks:
            skill_tasks = [
                f'Complete {sk} fundamentals course',
                f'Practice {sk} with hands-on exercises',
                f'Build a small {sk} project'
            ]
        
        core_children.append(make_step(
            f'{sk.title()} Mastery', 
            f'Develop proficiency in {sk} for {career_name}', 
            2, 
            known[:2] if i == 0 else [], 
            [f'Complete {sk} course', f'Build {sk} project', f'Pass {sk} assessment'],
            [f'{sk.title()} Course', f'{sk.title()} Documentation', f'{sk.title()} Practice Platform'],
            skill_tasks
        ))
    
    core = make_step(
        'Core Skills Development', 
        f'Master essential skills for {career_name}', 
        max(2, len(core_children)), 
        known, 
        ['Complete all core skill modules', 'Build skill demonstration projects', 'Pass skill assessments'],
        ['freeCodeCamp', 'Coursera', 'Udemy', 'LinkedIn Learning'],
        [
            'Create a skills tracking spreadsheet',
            'Set up practice projects for each skill',
            'Join skill-specific communities',
            'Find a mentor or study group',
            'Schedule regular skill assessments'
        ],
        children=core_children
    )

    project_children = [
        make_step(
            'Portfolio Project 1', 
            'Build a showcase project demonstrating core skills', 
            2, 
            known + missing[:2], 
            ['Complete project design', 'Implement core features', 'Deploy to GitHub Pages'],
            ['GitHub', 'Netlify/Vercel', 'Figma', 'Project documentation'],
            [
                'Research similar projects for inspiration',
                'Create project wireframes and design',
                'Set up project repository on GitHub',
                'Implement core functionality',
                'Write comprehensive README',
                'Deploy project and test functionality',
                'Create project presentation'
            ]
        ),
        make_step(
            'Portfolio Project 2', 
            'Build an advanced project showing specialization', 
            2, 
            known + missing[:3], 
            ['Complete advanced features', 'Add testing', 'Optimize performance'],
            ['GitHub', 'Testing frameworks', 'Performance tools', 'Documentation'],
            [
                'Choose a more complex project idea',
                'Plan project architecture',
                'Implement advanced features',
                'Add unit and integration tests',
                'Optimize for performance',
                'Create detailed documentation',
                'Prepare project demo'
            ]
        ),
    ]
    project = make_step(
        'Portfolio Development', 
        'Create impressive projects to showcase your skills', 
        len(project_children), 
        known, 
        ['Complete 2 portfolio projects', 'Deploy projects online', 'Create project presentations'],
        ['GitHub', 'Netlify', 'Vercel', 'Figma', 'Canva'],
        [
            'Research industry-standard project types',
            'Create project portfolio website',
            'Write detailed project case studies',
            'Prepare project demonstrations',
            'Get feedback from professionals'
        ],
        children=project_children
    )

    spec_children = [
        make_step(
            'Specialization Track A', 
            'Deep dive into primary specialization area', 
            2, 
            known + missing[:2], 
            ['Complete specialization course', 'Build specialization project', 'Write technical blog post'],
            ['Specialized courses', 'Industry blogs', 'Technical documentation', 'Community forums'],
            [
                'Research specialization requirements',
                'Complete advanced specialization course',
                'Build project demonstrating specialization',
                'Write technical blog post about specialization',
                'Join specialization-specific communities',
                'Attend specialization workshops/webinars'
            ]
        ),
        make_step(
            'Specialization Track B', 
            'Explore complementary specialization', 
            2, 
            known + missing[:2], 
            ['Complete secondary specialization', 'Create comparison analysis', 'Build hybrid project'],
            ['Secondary courses', 'Industry reports', 'Comparison tools', 'Documentation'],
            [
                'Research complementary specializations',
                'Complete secondary specialization course',
                'Create specialization comparison analysis',
                'Build project combining both specializations',
                'Document learning journey',
                'Share insights with community'
            ]
        ),
    ]
    spec = make_step(
        'Specialization Development', 
        'Develop expertise in specific areas of your field', 
        len(spec_children), 
        [], 
        ['Choose specialization tracks', 'Complete specialization projects', 'Build expertise portfolio'],
        ['Industry courses', 'Professional certifications', 'Technical blogs', 'Expert communities'],
        [
            'Research industry specialization trends',
            'Choose 2 complementary specializations',
            'Create specialization learning plan',
            'Build specialization projects',
            'Document specialization journey',
            'Connect with specialization experts'
        ],
        children=spec_children
    )

    job_children = [
        make_step(
            'Professional Branding', 
            'Create compelling professional presence', 
            1, 
            [], 
            ['Complete LinkedIn profile', 'Create professional resume', 'Build portfolio website'],
            ['LinkedIn', 'Canva', 'GitHub Pages', 'Resume builders', 'Portfolio templates'],
            [
                'Optimize LinkedIn profile with keywords',
                'Create professional headshot',
                'Write compelling professional summary',
                'Build comprehensive portfolio website',
                'Create resume tailored to target roles',
                'Develop personal brand statement',
                'Set up professional email signature'
            ]
        ),
        make_step(
            'Interview Preparation', 
            'Master technical and behavioral interviews', 
            1, 
            [], 
            ['Complete 50 practice questions', 'Mock interview sessions', 'Prepare STAR stories'],
            ['LeetCode', 'Pramp', 'InterviewBit', 'Glassdoor', 'YouTube interview prep'],
            [
                'Research common interview questions for role',
                'Practice technical problems daily',
                'Prepare STAR method stories',
                'Schedule mock interviews',
                'Study company-specific interview processes',
                'Practice coding on whiteboard',
                'Prepare questions to ask interviewers'
            ]
        ),
        make_step(
            'Job Search Strategy', 
            'Execute systematic job search campaign', 
            1, 
            [], 
            ['Apply to 50+ positions', 'Network with 20+ professionals', 'Track applications'],
            ['LinkedIn Jobs', 'Indeed', 'AngelList', 'Company websites', 'Networking events'],
            [
                'Create job search tracking spreadsheet',
                'Set up job alerts on multiple platforms',
                'Research target companies thoroughly',
                'Customize applications for each role',
                'Attend networking events and meetups',
                'Reach out to professionals for informational interviews',
                'Follow up on applications systematically'
            ]
        ),
    ]
    job = make_step(
        'Job Search & Application', 
        'Land your first role in the field', 
        len(job_children), 
        [], 
        ['Complete professional branding', 'Pass technical interviews', 'Receive job offers'],
        ['LinkedIn', 'Job boards', 'Interview platforms', 'Networking tools', 'Application tracking'],
        [
            'Develop comprehensive job search strategy',
            'Create application tracking system',
            'Build professional network',
            'Practice interview skills regularly',
            'Customize applications for each opportunity',
            'Follow up on all applications',
            'Negotiate offers professionally'
        ],
        children=job_children
    )

    # Tailor for focus
    if focus == 'Depth':
        core.duration_months += 1
    elif focus == 'Fast-Entry':
        project.duration_months += 1
    elif focus == 'Transition':
        job.duration_months += 1

    return [foundations, core, project, spec, job]


def generate_distinct_roadmaps(profile: Dict[str,Any], top_career: Dict[str,Any]):
    focuses = ['Depth','Fast-Entry','Transition']
    roadmaps = []
    for f in focuses:
        steps = generate_steps_for_career(top_career, profile.get('skills',[]), f, beginner=True)
        rm = Roadmap(path_title=top_career.get('career') or top_career.get('label', 'Career'), focus=f, confidence_score=0.8, steps=steps)
        roadmaps.append(rm)
    return roadmaps
