// Speakers configuration with bio and title information
const speakersConfig = {
  "hassan-sirelkhatim": {
    name: "Hassan Sirelkhatim",
    affiliation: "NVIDIA",
    title: "Revolutionizing AI-Driven Material Discovery Using NVIDIA ALCHEMI",
    image: "images/hassan-sirelkhatim.jpeg",
    linkedin: "https://www.linkedin.com/in/hassan-sirelkhatim/",
    bio: "Hassan Sirelkhatim is a Senior Solutions Architect with a focus on the intersection of machine learning and biology and chemistry. He has played a key role in advancing foundation models in areas such as nucleotides, proteins, and chemical structures. In his day-to-day work, he partners with customers to optimize their machine learning models for efficient performance on GPUs.",
    abstract: "The discovery of novel materials is central to addressing challenges in energy, sustainability, and advanced manufacturing. However, conventional computational approaches are often limited by their high computational cost. NVIDIA ALCHEMI (AI Lab for Chemistry and Materials Innovation) explores new R&D directions to accelerate this process. A central innovation is Batched approach to simulation on which machine learning interatomic potentials (e.g., MACE, AIMNet2) achieve speedups of up 100x. By exploiting inference batching, GPU-native kernels, and CUDA-optimized libraries, ALCHEMI demonstrates how modern AI and HPC can be combined to deliver accurate, scalable, and physically consistent methods for chemical and materials discovery."
  },
  "peter-coveney": {
    name: "Prof. Peter Coveney",
    affiliation: "UCL",
    title: "The Wall Confronting Large Language Models",
    image: "images/peter-coveney.jpg",
    linkedin: "https://profiles.ucl.ac.uk/3406-peter-coveney",
    bio: "Peter Coveney is a Professor of Physical Chemistry at UCL. He is a Fellow of the Royal Academy of Engineering and Member of Academia Europaea. Coveney is active in a broad area of interdisciplinary research including condensed matter physics and chemistry, materials science, as well as human digital twins in healthcare and quantum computing applications. Dr Coveney has published well over 500 scientific papers and is the author of Virtual You (2023).  His latest book, Molecular Dynamics: Probability and Uncertainty (with Shunzhou Wan) was published on 15 May 2025.",
    abstract: "The scaling laws which determine the performance of large language models severely limit their ability to reduce the uncertainty of their predictions. Raising their reliability by brute force is intractable since the mechanism which fuels much of the learning power of LLMs also underpins error pileup. These issues also afflict large-reasoning models and agentic AI approaches which seek to provide more reliable and better informed outputs than the LLMs from which they are derived. It is essential to establish better metrics reflecting the verifiability and reliability of the predictions emanating from these and related forms of artificial intelligence systems."
  },
  "james-gin": {
    name: "James Gin-Pollock",
    affiliation: "Orbital Materials",
    title: "Generate • Simulate • Reason: Chaining Foundation Models to Discover Materials",
    image: "images/james-gin.jpg",
    linkedin: "https://www.linkedin.com/in/jamesgin/?originalSubdomain=uk",
    bio:"James leads the computational research team at Orbital Materials, a Series A funded and NVIDIA-backed startup which is developing new materials and technologies for the energy transition. Orbital's notable projects include a dual-use data centre chiller which captures ambient CO2 using waste heat, developed as a strategic partner of AWS, a two-phase GPU cooling system powered by a novel non-PFAS dielectric fluid, and the open-source machine learning interatomic potential Orb. His background is in physics and machine learning, and as an entrepreneur has founded several AI companies, one of which was acquired by Shutterstock.",
    abstract:"At Orbital Materials we accelerate materials discovery using a range of in-house foundation models - including Orb, a universal ML interatomic potential for fast, accurate simulation; diffusion-based models for steerable generation of crystal structures; and LLMs for orchestration of material science workflows. I'll show how we built Orb, and how MLIPs and generative models are two views of the same energy landscape, connected by the Boltzmann distribution. We'll discuss practical considerations for deploying structure generative models and how missing benchmarks stall progress. Finally we'll show how LLMs can orchestrate other foundation models to accelerate real world research."
  },
  "francesco-ferroni": {
    name: "Dr. Francesco Ferroni",
    affiliation: "NVIDIA",
    title: "NVIDIA Cosmos: World Foundation Models for Physical AI",
    image: "images/francesco-ferroni.jpg",
    linkedin: "https://www.linkedin.com/in/francesco-ferroni/",
    bio:"Francesco Ferroni is a Principal Research Scientist at NVIDIA, leading the Deep Imagination Research team. His work focuses on world foundation models (WFMs) for physical AI, spanning video generation, multimodal reasoning, and simulation for robotics and autonomous systems. Previously, he led deep learning teams at Argo AI and holds a PhD in Computational Physics from the University of Oxford.",
    abstract:"This talk explores NVIDIA Cosmos, a platform for developing world foundation models that power physical AI. Francesco will introduce the Cosmos Predict, Transfer, and Reason models—unifying video generation, controllable simulation, and multimodal reasoning. Attendees will learn how Cosmos bridges large-scale data curation, GPU-accelerated training, and real-world deployment to advance robotics and embodied intelligence."
  },


  "steven-kench": {
    name: "Dr. Steven Kench",
    affiliation: "Polaron",
    title: "Foundational models for materials manufacturing",
    image: "images/steven-kench.jpg",
    linkedin: "https://www.linkedin.com/in/steve-kench-a26a2a2b1/",
    bio:"Steve Kench completed his PhD at Imperial College London, where he developed generative machine learning methods for battery electrode design. He is now the CTO of Polaron, leading the creation of image-based AI tools for material science. His work centres on microstructural characterisation and the optimisation of manufacturing processes using small, efficient models trained on limited datasets. Steve is passionate about building AI workflows that are both powerful and practical, helping scientists and engineers accelerate R&D, enhance manufacturing efficiency, and uncover new material designs.",
    abstract:"Foundational models have transformed fields like language and vision — but materials manufacturing presents a unique challenge. Data is scarce, heterogeneous, and governed by complex physical laws. This talk explores the path toward a foundational model for materials: one that learns from images, process parameters, and structure–property relationships to understand, control, and optimise manufacturing. It will outline the key ingredients — multimodal data integration, physics-informed learning, and scalable yet efficient architectures — and discuss how such systems could unify fragmented datasets, accelerate discovery, and transform the way advanced materials are designed and produced."
  },
  "sina-samangooei": {
    name: "Dr. Sina Samangooei",
    affiliation: "CuspAI",
    title: "The CuspAI Platform: Foundation Models, Search, and Agents for Materials Discovery",
    image: "images/sina-samangooei.jpg",
    linkedin: "https://www.linkedin.com/in/sinjax/?originalSubdomain=uk",
    bio:"Sina Samangooei builds multimodal AI systems for materials discovery at CuspAI. Previously at Google DeepMind worked on Gemini and multimodal models, and before that led computer vision for autonomous vehicles at FiveAI. PhD from Southampton in biometrics and multimodal learning. Enjoys hacking on LLMs and distributed ML infrastructure. Lives in Cambridge with partner Em and two kids.",
    abstract: "Sustainable materials discovery demands AI systems that bridge generation, search, and reasoning with computational chemistry and experimental validation. CuspAI is developing an integrated platform targeting carbon capture and beyond. I'll overview our architecture—generative models, computational tools, property predictors—before discussing our foundation model work: multimodal training combining text and MLIPs, vector search over material structures. The main focus of the talk will be LLM agents: how we're building intelligent orchestration systems that coordinate discovery workflows, make reasoning decisions about which computational tools to deploy, and integrate generation, search, and validation. I'll demonstrate how these agents transform our platform from disconnected tools into a cohesive discovery engine driving materials from hypothesis to synthesis."
  },
  "lei-ge": {
    name: "Lei Ge",
    affiliation: "Imperial College London",
    title: "Do Llamas understand the periodic table?",
    image: "images/lei-ge.JPG",
    linkedin: "https://www.linkedin.com/in/ge-lei-04706b28b/?originalSubdomain=uk",
    bio:"Lei Ge is a PhD student at Imperial College London specializing in large language models (LLMs) for materials science. Her research explores how LLMs interpret and reason about chemical knowledge to improve explainability, and how LLM-based agents can be designed to accelerate materials optimization and scientific discovery. Alongside her doctoral studies, she works as a part-time Machine Learning Engineer at Polaron, applying her expertise to real-world AI applications.",
    abstract: "LLMs are increasingly used in materials science for hypothesis generation and knowledge discovery. However, how these models encode specialized scientific knowledge remains unclear. We examine how the open-source Llama models represent the periodic table of elements. By visualizing hidden-state embeddings, we observe a three-dimensional spiral structure that mirrors the conceptual organization of the periodic table. Linear probing further shows that intermediate layers encode continuous, overlapping attributes that enable indirect recall, while deeper layers refine categorical distinctions and integrate linguistic context. These findings suggest that LLMs represent scientific knowledge not as discrete symbols, but as geometric manifolds that intertwine semantics and structure across layers. Our results provide new insight into how LLMs internalize scientific concepts, offering pathways toward improved interpretability, model reliability, and the integration of AI tools in materials discovery."
  },
  "ronan-docherty": {
    name: "Ronan Docherty",
    affiliation: "Imperial College London",
    title: "Make do and mend: leveraging vision transformers for micrograph segmentation",
    image: "images/ronan-docherty.jpg",
    linkedin: "https://www.linkedin.com/in/ronan-docherty-3812ab2b0/",
    bio: "Ronan is a PhD student at Imperial College London working on using modern machine learning techniques to improve micrograph segmentation. He also works part-time at Polaron as a machine learning engineer.",
    abstract: "Segmentation - the assigning of a class to every pixel in an image - is a prerequisite for many kinds of downstream analysis in materials science. Modern computer vision has tended towards foundation models, usually in the form of vision transformers trained on massive datasets of natural images. These models offer impressive performance on benchmarks, encode rich information about the structure and content of images, and are the result of expensive training campaigns. This talk focuses on how to adapt these foundation models for segmentation of materials micrographs, where we often suffer from a lack of data (labelled or otherwise), heavily out-of-distribution images, and the need to capture very fine features."
  }
};

// Talk order for the schedule (8 talks total)
// Simply reorder this array to change the schedule
const talkOrder = [
  "hassan-sirelkhatim",  // Talk 1: 10:05 – 10:50
  "peter-coveney",       // Talk 2: 10:50 – 11:35
  "lei-ge",              // Talk 3: 12:05 – 12:30
  "ronan-docherty",      // Talk 4: 12:30 – 12:55
  "james-gin",           // Talk 5: 14:10 – 14:55
  "steven-kench",        // Talk 7: 16:10 – 16:55
  "sina-samangooei",     // Talk 8: 16:55 – 17:40
  "francesco-ferroni",   // Talk 6: 14:55 – 15:40

];
