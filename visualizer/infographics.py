import os
import subprocess
from typing import Dict, Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class InfographicGenerator:
    def __init__(self,
                 code_model='gemini-1.5-flash-8b',):
        """
        Initialize the infographic generator with open-source AI models
        """

        self.model = code_model
        # Code Generation Model
        self.llm = ChatGoogleGenerativeAI(model=self.model)

        # Output directory
        self.output_dir = 'infographic_outputs'
        os.makedirs(self.output_dir, exist_ok=True)

    def preprocess_data(self, input_data: str) -> Dict[str, Any]:
        """
        Preprocess and analyze input data
        """
        # First, clean and normalize the input
        cleaned_data = input_data

        # Use NLP to understand data context
        context_analysis = self.llm.invoke(f"""
        Analyze the following data and provide:
        1. Data type (percentages, comparisons, time series, etc.)
        2. Key statistical insights
        3. Suggested visualization type

        Data: {cleaned_data}
        """)

        print(context_analysis.content)

        return {
            'raw_data': cleaned_data,
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

        print(viz_recommendation.content)
        return viz_recommendation.content

    def generate_manim_code(self,
                             data_analysis: Dict[str, Any],
                             viz_type: str) -> str:
        """
        Generate Manim animation code dynamically
        """
        manim_code_prompt = f"""
        Generate Matplotlib Python code for a {viz_type} visualization with these requirements:
        - Data: {data_analysis['raw_data']}
        - Create an animated, professional visualization
        - Use a clean, modern color palette
        - Include smooth transitions
        - Add clear labels and title

        Provide ONLY the complete Matplotlib scene class code. DO NOT USE MARKDOWN syntax. DO NOT USE THREE BACKTICKS
        """

        manim_code = self.llm.invoke(manim_code_prompt)
        print(manim_code.content)
        return manim_code.content

    def render_visualization(self, manim_code: str, output_filename: str):
        """
        Render the Manim visualization to video
        """
        try:
            # Dynamically create a Python file with the Manim scene
            with open('temp_manim_scene.py', 'w') as f:
                f.write(manim_code)

            # Render the scene
            try:
                subprocess.run(['python',  'temp_manim_scene.py'], stdout=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError as e:
                print(e.cmd)
                print(f"Command failed with exit code: {e.returncode}")
                print(f"Error: {e.stderr}")

            # Move output to designated folder
            os.rename(
                f'media/videos/temp_manim_scene/1080p60/Scene.mp4',
                os.path.join(self.output_dir, output_filename)
            )

            print(f"Visualization rendered: {output_filename}")
        except Exception as e:
            print(f"Error rendering visualization: {e}")

    def generate_infographic(self, prompt: str):
        """
        Main pipeline for generating infographic video
        """
        # preprocess and analyze data
        data_analysis = self.preprocess_data(prompt)

        # recommend visualization type
        viz_type = self.recommend_visualization(data_analysis)

        # generate Manim animation code
        manim_code = self.generate_manim_code(data_analysis, viz_type)

        # render visualization
        output_filename = f'infographic_{len(os.listdir(self.output_dir)) + 1}.mp4'
        self.render_visualization(manim_code, output_filename)

        return os.path.join(self.output_dir, output_filename)
