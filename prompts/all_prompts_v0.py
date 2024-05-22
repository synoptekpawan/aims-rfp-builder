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
        Instructions:
        - Overview of the proposed partnership.
        - Unique value proposition offered by Synoptek.
        - Projection of costs, incentives, and financial benefits.
        - Summary of ongoing support and resources.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'cover_letter': """
        Enhance the provided text for a technical cover letter. Address:
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
        Develop a technical background from provided text. Ensure a detailed presentation:
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'business_objective': """
        Create a detailed business objective from provided text, focusing on:
        - Innovative program features.
        - Capabilities for future-proofing by Synoptek.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'opportunities_and_challenges': """
        Detail the technical opportunities and challenges from provided text:
        - Client-specific and common challenges.
        - Strategic partnership goals focusing on client benefits.
        - Critical success factors for global team effectiveness.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'scope_of_work': """
        Create a technical scope of work from provided text, outlining specific tasks:
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'deliverables': """
        Describe technical deliverables from provided text, detailing:
        - Expected outputs.
        - Project milestones.
        - Required documentation and client-specific requirements.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'synoptek_approach': """
        Outline a technical approach under the theme "Envision, Transform, Evolve":
        - Envision: Planning and objectives.
        - Transform: Implementation processes.
        - Evolve: Continuous improvement.
        ---
        Here is the example of extracted text:\n{extracted_text}
        Here is additional information:\n{scope}
        """,

        'transition_plan': """
        Develop a technical transition plan detailing:
        - Introduction to the transition.
        - Transition approach and methodologies.
        - Key transition activities and milestones.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """,

        'timeline': """
        Craft a technical timeline plan table:
        - Introduction to Timeline.
        - Detailed tabular Timeline.
        ---
        Here is the example of extracted text:\n{extracted_text}
        """
    }
