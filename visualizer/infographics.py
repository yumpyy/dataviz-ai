import os
import re
import subprocess
from typing import Dict, Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class InfographicGenerator:
    def __init__(self,
                 model='gemini-1.5-flash',):
        """
        initialize the infographic generator with open-source ai models
        """

        self.model = model
        # code generation model
        self.llm = ChatGoogleGenerativeAI(model=self.model)

        # output directory
        self.output_dir = 'static/videos/'
        os.makedirs(self.output_dir, exist_ok=True)

    def preprocess_data(self, input_data: str) -> Dict[str, Any]:
        """
        preprocess and analyze input data
        """

        # use llm to understand data context
        context_analysis = self.llm.invoke(f"""
        Analyze the following data and provide:
        1. Data type (percentages, comparisons, time series, etc.)
        2. Key statistical insights
        3. Suggested visualization type

        Data: {input_data}
        """)

        return {
            'raw_data': input_data,
            'context': context_analysis.content
        }

    def recommend_visualization(self, data_analysis: Dict[str, Any]) -> str:
        """
        Recommend the most appropriate visualization type
        """
        viz_recommendation = self.llm.invoke(f"""
        Based on this data analysis, recommend the best visualization type:
        {data_analysis['context']}

        Possible types:
        - Pie Chart
        - Bar Graph
        - Line Graph
        - Histogram
        - Scatter Plot

        Respond with ONLY the visualization type.
        """)

        return viz_recommendation.content

    def generate_manim_code(self,
                             data_analysis: Dict[str, Any],
                             viz_type: str) -> str:
        """
        generate manim animation code dynamically
        """
        manim_code_prompt = f"""
        You are an extremely skilled, highly paid professional developer/animator

        Generate Manim Python code for a {viz_type} visualization with these requirements:
        - Data Summary: {data_analysis['context']}
        - Create an animated, professional visualization
        - Use a clean, modern color palette
        - Include smooth transitions
        - Add clear labels and title
        - Make sure to have all library import statements
        - Code should be error-free

        Avoid using these symbols: $, ```

        We will be directly executing your code. It should be executable without having to change anything to code. So make sure the code is complete. Do not expect any human intervention
        Provide ONLY the complete Manim scene code. DO NOT USE MARKDOWN CODE BLOCK OR ANYTHING ELSE
        """

        manim_code = self.llm.invoke(manim_code_prompt)

        clean_code = re.sub(r'```python|```', '', manim_code.content)

        return clean_code

    def render_visualization(self, manim_code: str, output_filename: str):
        """
        render the manim visualization to video
        """
        try:
            # dynamically create a python file with the manim scene
            with open('temp_manim_scene.py', 'w') as f:
                f.write(manim_code)

            # render the scene
            try:
                subprocess.run(['manim', '-o', 'temp', 'temp_manim_scene.py'], stdout=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError as e:
                print(e.cmd)
                print(f"Command failed with exit code: {e.returncode}")
                print(f"Error: {e.stderr}")

                return False

            # move output to designated folder
            os.rename(
                f'media/videos/temp_manim_scene/1080p60/temp.mp4',
                os.path.join(self.output_dir, output_filename)
            )

            print(f"Visualization rendered: {output_filename}")

            return True

        except Exception as e:
            print(f"Error rendering visualization: {e}")
            return False

    def generate_infographic(self, prompt: str):
        """
        generate infographic video
        """
        # preprocess and analyze data
        data_analysis = self.preprocess_data(prompt)

        # recommend visualization type
        viz_type = self.recommend_visualization(data_analysis)

        # generate Manim animation code
        manim_code = self.generate_manim_code(data_analysis, viz_type)

        # render visualization
        output_filename = f'{len(os.listdir(self.output_dir)) + 1}.mp4'
        if self.render_visualization(manim_code, output_filename) == False:
            # if an error occurs, return None
            return None

        return 'videos/' + output_filename
