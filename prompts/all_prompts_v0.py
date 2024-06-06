def prompts_():
    return {
        'table_of_contents': """
        Objective: Create a structured and detailed Table of Contents from provided text for a comprehensive business report. The Table of Contents should provide a clear and easy navigation system for readers, enabling them to quickly locate information within the document.
        
        Instructions:
        - Identify Main Sections: List all primary sections of the business report, such as Executive Summary, Introduction, Market Analysis, Services Offered, etc.
        - Subsections: Under each main section, identify necessary subsections like Industry Overview, Competitive Analysis, and Target Market.
        - Page Numbers: Assign logical starting page numbers to each section and subsection.
        - Formatting: Use clear formatting. Main sections should be bolded, and subsections indented.
        - Additional Elements: Include elements like Appendices, Glossary, and References, indicating their locations.
        ---
        Here is the example of provided text:\n{list_of_sections}
        """,

        'executive_summary': """
        Objective: Create a technical executive summary based on provided text.
        Don't add any AT created message at start and end of response. 
        Instructions:
        - Overview of the proposed partnership.
        - Unique value proposition offered by Synoptek.
        - Projection of costs, incentives, and financial benefits.
        - Summary of ongoing support and resources.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'cover_letter': """
        Enhance the provided text for a technical cover letter.
        Don't add any AT created message at start and end of response.
        - Appreciation and topic introduction.
        - Understanding client needs.
        - Unique qualifications of Synoptek.
        - Specific services and solutions offered.
        - Future collaboration opportunities.
        - Closing remarks.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'background': """
        Develop a technical background from provided text. Ensure a detailed presentation.
        This section should include a brief description of the client company and what they do. 
        The project background should include information about the reasoning why you want to implement this specific project in the specific manner.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'business_objective': """
        Create a detailed business objective from provided text. It should focus on:
        - What the client is hoping to accomplish from a business perspective (non-technical):
            - Goal: Write a high-level project goal and provide context to the business value and functional achievements.
            - Objectives: Write specific objectives, summarizing the reason for the project, intent and key tasks intended to be achieved by the project. 
              Focus on non-technical business objectives.
        - Innovative program features.
        - Capabilities for future-proofing by Synoptek.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'opportunities_and_challenges': """
        Detail the technical opportunities and challenges from provided text.
        It must explain the current situation, its pain points, and the way in which the project solution will solve these problems. 
        This section should include:
        - A history of the problem as it relates to our business.
        - A concise summary of the project's requirements.
        - Some details about the business purpose of the project 
        - Client-specific and common challenges.
        - Strategic partnership goals focusing on client benefits.
        - Critical success factors for global team effectiveness.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'scope_of_work': """
        Create a technical scope of work from provided text, outlining specific tasks.
        Project Scope of Work is a culmination of common elements from objectives, scope, major milestone, tasks supporting the milestones, which teams are responsible for completing work and if applicable provide a summary/estimated schedule.
        This section addresses any kind of functional / non-functional project requirements to be catered to while taking up the project / discovery. This will help in ring-fencing the overall scope of the project under contract. It becomes essential when proposing Fixed cost projects.
        - High level features of the solution and how it will be carried out.
        - List the business processes, departments, applications, and data sources that are in scope for this project.
        - Do not add a very detailed explanation about the requirement but at the same time, write understandable and concise requirement statements specific to the client's unique situation.

        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'deliverables': """
        Describe technical deliverables from provided text, detailing:
        - Expected outputs.
        - Project milestones.
        - Required documentation and client-specific requirements.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'synoptek_approach': """
        Outline a technical approach under the theme "Envision, Transform, Evolve":
        - Envision: Planning and objectives.
        - Transform: Implementation processes.
        - Evolve: Continuous improvement.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        Here is additional information:\n{scope}
        """,

        'transition_plan': """
        Develop a technical transition plan detailing:
        - Introduction to the transition.
        - Transition approach and methodologies.
        - Key transition activities and milestones.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'timeline': """
        Craft a technical timeline plan table:
        - Introduction to Timeline.
        - Detailed tabular Timeline.
        Don't add any AT created message at start and end of response.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """
    }
