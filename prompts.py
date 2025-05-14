

def cover_letter_prompt(job_description):
    """
    This function generates a prompt for creating a cover letter based on the provided job description and resume.
    
    Returns:
        str: The generated prompt for the cover letter.
    """
    COVER_LETTER_PROMPT = f"""Compose a brief and impactful cover letter based on the provided job description and resume. The letter should be no longer than three paragraphs and should be written in a professional, yet conversational tone. Avoid using any placeholders, and ensure that the letter flows naturally and is tailored to the job.

        Analyze the job description to identify key qualifications and requirements. Introduce the candidate succinctly, aligning their career objectives with the role. Highlight relevant skills and experiences from the resume that directly match the job’s demands, using specific examples to illustrate these qualifications. Reference notable aspects of the company, such as its mission or values, that resonate with the candidate’s professional goals. Conclude with a strong statement of why the candidate is a good fit for the position, expressing a desire to discuss further.

        Please write the cover letter in a way that directly addresses the job role and the company’s characteristics, ensuring it remains concise and engaging without unnecessary embellishments. The letter should be formatted into paragraphs and should not include a greeting or signature.

        ## Rules:
        - Do not include any introductions, explanations, or additional information. output the cover letter in latex format, and do not include any greeting or signature.

        ## Details :

        - **My resume:**
     
        Education University of Stuttgart Oct 2021 – Nov 2024 Department of Computer Science, Electrical Engineering and Information Technology GPA: 1,5/1,0 (very good) Major: Electromobility (Autonomous and Connected Driving) China University of Petroleum Sep 2017 – June 2021 B.Sc Vehicle Engineering GPA: 89.8/100; Ranking: 5/113 Relevant Coursework Deep Learning (grade 1,0); Matrix Computations in Signal Processing and Machine Learning (grade 1,0); Advanced mathematics for signal and information processing (grade 1,0); Computer Vision (grade 1,0); Research Thesis (grade 1,0); Master Thesis (grade 1,0) Award Outstanding Graduate of China University of Petroleum, 2 times First-Class Scholarship for Academic Excellence Skills Programming: Python (proficient), C++ (proficient), Swift (intermediate) Machine learning framework: Pytorch, Tensorflow, NumPy, Pandas, OpenCV, Matplotlib; Experience with ML related algorithms and corresponding mathematics: Classification, Segmentation, Recognition and Generation tasks; GAN, Diffusion, Transformer; Probability Theory, Optimization, Matrix Computation, etc Medical image processing: Nibabel, SimpleITK Tools: Git, SLURM, LATEX, Docker, Azure DevOps, CI/CD, MATLAB, Auto-CAD, Solidworks, Catia, Microsoft Office Operating System: Linux, ROS, Mac OS, Windows Languages: English (Fluent, C1), German (Verhandlungssicher, Goethe Zertifikat C1 (gut), DSH-3), Chinese (Native) Publication [1] Mayar Elfares, Pascal Reisert, Zhiming Hu, Wenwu Tang, Ralf K¨usters, Andreas Bulling. PrivatEyes: Appearance-based Gaze Estimation Using Federated Secure Multi-Party Computation, Proceedings of the ACM on Human-Computer Interaction, 2024 Projects Master Thesis | Institute of Signal Processing and System Theory Mar 2024 – Oct 2024 Supervisors: Prof. Dr.-Ing. Bin Yang, M.Sc. Khaled Seyam, Dr. George Eskandar Topic: Towards 3D Semantic Image Synthesis for Medical Imaging • This topic is an extension of my research thesis. I propose a Latent Semantic Diffusion Model (LSDM) to solve 3D Semantic Image Synthesis problem in Medical Domain. I implement VQ-GAN model to map the 3D medical images to a discrete latent space, then 3D Semantic Diffusion Model is implemented in this latent space. In the end, the data is re-mapped to image space using pre-trained decoder of VQ-GAN. Our approach can significantly reduce the computational requirement while achieving high quality 3D semantic image synthesis in AutoPET, Duke Breast and SynthRAD2023 datasets. Research Thesis | Institute of Signal Processing and System Theory June 2023 – Feb 2024 Supervisors: Prof. Dr.-Ing. Bin Yang, Dr. George Eskandar Topic: Unsupervised Semantic Image Synthesis for Medical Imaging • We propose a GAN-based framework Med-USIS, which can synthesize MRI images based on CT semantic maps in a unsupervised paradigm. Deep learning-based generative models and domain adaptation methods are utilized to achieve accurate and reliable semantic map translation. Human Activity Recognition | Institute of Signal Processing and System Theory Supervisors: Prof. Dr.-Ing. Bin Yang, M.Sc. Mario D¨obler Topic: A Full-Stack project that includes Data Collection, Pre-Processing, Model Training, and Real-Time Deployment • Develop a iOS-based application called HumanActivityRecorderApp for real-time human activity Data Collection, supporting sensor Data Collection, Manual Labeling, and data export to build dataset. • Train a Deep Learning Model using collected Accelerometer and Gyroscope data, and converted it to CoreML. • Develop a iOS app called HumanActivityClassifierApp and Deploy the model with custom animated line charts for live sensor feedback. Experience Autonomous Driving Software Engineer Intern | Momenta Europe GmbH Aug 2024–Now System R&D Group Topics: Work on the Momenta L2++ Cruise Pilot product for Mercedes New CLA prototype • Develop and maintain Advanced Data Mining and Simulation Software to automate the mining, curating, ingesting and managing high quality scenario libraries, encompassing a variety of driving scenarios, which can be used to train models and evaluate software performance changes through offline simulations. • Design and implement SLIF(Speed Limit Information Function) Evaluation Software to validate the performance of traffic sign recognition effectively. • Responsible for the development and iteration of Checkers for scenario simulation loops tailored to European requirements. Quality inspection of annotations for overseas-specific data and provide guidance to road test engineers during the annotation process. • Coordinate data collection campaigns with internal and external data collection teams, analyzing AD system problems in real vehicle test and offline simulation test, coordinating the teams responsible for each algorithm modules. • Supporting the adaptation of Advanced Assisted Driving Systems for China’s electric vehicles (SAIC IM) to align with European standards and pass regulatory requirements tests. Student Research Assistant | Institute of Human-Computer Interaction and Cognitive Systems Jun 2024–Nov 2024 Supervisors: Prof. Dr. Andereas Bulling, Dr. Lei Shi Topics: ActionDiffusion: An Action-aware Diffusion Model for Procedure Planning in Instructional Videos • Implement Foundation Model(Video-Language Model (VLM)) to extract video features and action embeddings of three instructional video benchmark datasets (CrossTask, Coin and NIV), and train the ActionDiffusion model for procedure planning Student Research Assistant | Institute of Human-Computer Interaction and Cognitive Systems Apr 2023–Dec 2023 Supervisors: Prof. Dr. Andereas Bulling, M.Sc. Mayar Elfares Topics: PrivatEyes: Appearance-based Gaze Estimation Using Federated Secure Multi-Party Computation • We propose the first privacy-enhancing training approach for appearance-based gaze estimation methods based on federated learning and secure multi-party computation. Implement Generative Model-Inversion and Dataset Inference methods to attack and test our method on MPIIGaze, MPIIFaceGaze, GazeCapture, and NVGaze benchmark datasets. This paper has been accepted by ETRA 2024.
        
        - **Job Description:**

        {job_description}

        """
        
    return COVER_LETTER_PROMPT


def summary_job_description(job_description):
    """
    This function generates a summary of the job description using a predefined prompt.
    
    Args:
        job_description (str): The job description to summarize.
        
    Returns:
        str: The generated summary of the job description.
    """
    
    JOB_SUMMARY_PROMPT = f"""
    As a seasoned HR expert, your task is to identify and outline the key skills and requirements necessary for the position of this job. Use the provided job description as input to extract all relevant information. This will involve conducting a thorough analysis of the job's responsibilities and the industry standards. You should consider both the technical and soft skills needed to excel in this role. Additionally, specify any educational qualifications, certifications, or experiences that are essential. Your analysis should also reflect on the evolving nature of this role, considering future trends and how they might affect the required competencies.

    Rules:
    Remove boilerplate text
    Include only relevant information to match the job description against the resume

    # Analysis Requirements
    Your analysis should include the following sections:
    Technical Skills: List all the specific technical skills required for the role based on the responsibilities described in the job description.
    Soft Skills: Identify the necessary soft skills, such as communication abilities, problem-solving, time management, etc.
    Educational Qualifications and Certifications: Specify the essential educational qualifications and certifications for the role.
    Professional Experience: Describe the relevant work experiences that are required or preferred.
    Role Evolution: Analyze how the role might evolve in the future, considering industry trends and how these might influence the required skills.

    # Final Result:
    Your analysis should be structured in a clear and organized document with distinct sections for each of the points listed above. Each section should contain:
    This comprehensive overview will serve as a guideline for the recruitment process, ensuring the identification of the most qualified candidates.

    # Job Description:
    {job_description}

    """
    return JOB_SUMMARY_PROMPT