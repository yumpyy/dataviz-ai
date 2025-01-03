import os
import re
import subprocess
from typing import Dict, Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class InfographicGenerator:
    def __init__(self,
                 model='gemini-2.0-flash-exp',):
        """
        initialize the infographic generator with open-source ai models
        """

        self.model = model
        # code generation model
        self.llm = ChatGoogleGenerativeAI(model=self.model,)

        # output directory
        self.output_dir = 'static/videos/'
        os.makedirs(self.output_dir, exist_ok=True)

    def preprocess_data(self, input_data: str) -> Dict[str, Any]:
        """
        preprocess and analyze input data
        """

        input_data = input_data.strip()

        # use llm to understand data context
        context_analysis = self.llm.invoke(f"""
        Analyze the following data and provide:
        1. Data type (percentages, comparisons, time series, etc.)
        2. Key statistical insights
        3. And other additional information which may come handy while animating.
        4. Suggest ONLY a single visualization type

        Data: {input_data}
        """)

        print(context_analysis.content)
        return {
            'raw_data': input_data,
            'context': context_analysis.content
        }

    def generate_infographic_scenes(self, data_analysis):
        # define the prompt for generating infographic animation scenes
        prompt = f"""
            Generate scenes for infographic animations. Keep the visuals really basic, so that manim code can be easily generated for it.
            Summary: {data_analysis['context']}

            Here is an example:
            Input: Tech company revenue growth: 2020: $100M, 2021: $150M, 2022: $220M
            Output: ['Scene 1: X and Y axis for graph are emerging', 'Scene 2: Labels appear on the axis', 'Scene 3: bars rising up from x axis', 'Scene 4: Labels appear on top of each']

            Input: Sales percentages of a store's top three product categories: Electronics: 40%, Clothing: 30%, Groceries: 30%
            Output: ['Scene 1: A pie chart circle emerges', 'Scene 2: Segments appear with colors for each category', 'Scene 3: Labels with percentages fade in near each segment']
            
            Input: Monthly website visitors: January: 20K, February: 25K, March: 30K
            Output: ['Scene 1: X and Y axes appear for a line graph', 'Scene 2: Points appear on the graph for each month', 'Scene 3: A line connects the points, showing the trend', 'Scene 4: Labels for months and visitor counts fade in']
            
            Input: Task completion in a project: Completed: 70%, Pending: 20%, Delayed: 10%
            Output: ['Scene 1: A circle appears and divides into three segments for a pie chart', 'Scene 2: Each segment is color-coded and labeled', 'Scene 3: Arrows point outward from each segment to percentages shown']
            
            Input: Population distribution by age groups: Children: 25%, Adults: 60%, Seniors: 15%
            Output: ['Scene 1: A horizontal bar chart emerges with three categories', 'Scene 2: Bars grow proportionally to the percentages', 'Scene 3: Labels appear beside each bar']
            
            Input: Quarterly profits: Q1: $50M, Q2: $80M, Q3: $90M, Q4: $120M
Output: ['Scene 1: A bar chart grid with X and Y axes fades in', 'Scene 2: Bars for each quarter rise in sequence', 'Scene 3: Profit values appear above each bar', 'Scene 4: A title for the chart fades in']

        Do not include any additional text or explanations.
        """
        response = self.llm.invoke(prompt)

        # filter out markdown syntax if reponse has one
        response = re.sub(r'```python|```', '', response.content)

        return response

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
                            scene: str,
                            ) -> str:
        """
        generate manim animation code dynamically
        """

        manim_code_prompt = f"""
You are a great animator who uses manim to create very beautiful and perfect visuals with differnet fonts and colors

Prompt:

Given the following context:

    Data: {data_analysis['context']}
    Scene Description: {scene}

Task:
Create a Manim Python scene that generates an animated, creative visualization adhering to these guidelines:

    Visual Style:
        Clean, Pastel color palette
        Background and foreground colors shall not overlap
        Use color=ManimColor('#hexcodehere')
        Smooth transitions
        Clear labels and title
    Functionality:
        Accurate data representation based on the provided scene
    Code Constraints:
        No external files to be used. Including images, videos, gifs or anything else.
        Library Imports: Use only the specified libraries
        Code Completeness: Ensure the code is executable without modifications
    Output Format:
        Provide the complete Manim scene code directly, without any formatting or additional elements.

Please avoid using the symbols $ and ``` in your response.
        """

        manim_code = self.llm.invoke(manim_code_prompt)

        # filter out markdown syntax if reponse has one
        clean_code = re.sub(r'```python|```', '', manim_code.content)

        return clean_code

    def create_svg(self, manim_code: str):
        """
        create assets for the code, if any.
        """

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

        # generate scenes
        scenes = self.generate_infographic_scenes(data_analysis)
        print(scenes)

        # for scene in scenes:
        manim_code = self.generate_manim_code(data_analysis, scenes,)

        # render visualization
        output_filename = f'{len(os.listdir(self.output_dir)) + 1}.mp4'

        if self.render_visualization(manim_code, output_filename) == False:
            # if an error occurs, return None
            return None

        return 'videos/' + output_filename
