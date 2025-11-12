## Reflection Engagement

### What Worked Well
The dual-agent design between the **Planner Agent** and the **Reviewer Agent** worked smoothly.  
The Planner Agent generated natural, day-by-day itineraries that reflected user interests, pacing, and budget without relying on the internet. The structured format with clear time-based sections (Morning, Afternoon, Evening, Estimated Cost) improved readability and user experience.  
The Reviewer Agent effectively verified the itinerary using the `internet_search` tool, checking for realistic timing, transportation, and pricing. Its “Delta List” and “Improved Summary” provided targeted, actionable feedback that enhanced the overall plan quality.

---

### What Could Be Improved
One challenge was controlling Markdown rendering and spacing in Streamlit.  
Early outputs showed issues like unwanted italics and dense formatting. To fix this, I refined the prompt to remove Markdown syntax and used CSS to improve spacing, paragraph clarity, and font readability.  
Additionally, the Reviewer sometimes focused too much on writing style rather than factual validation. Future improvements could include making its feedback more data-driven and connecting the Delta List directly to Planner re-generation for smoother iteration.

---

### What Was Learned
This project highlighted the importance of **prompt engineering precision** and **role clarity** in multi-agent systems.  
Even small formatting details in prompts can affect readability and overall user perception.  
Separating creative generation (Planner) and factual validation (Reviewer) made the system modular and reliable.  
Overall, I learned that effective AI collaboration depends on prompt structure, agent coordination, and user-centered output design.

