
Methodology
=====


Introduction
*******************

Imagine we have a simulation where there are 10 agents, and we want to model the spread of a disease like COVID-19. 
In this simulation, we will run it for 5 time steps (``K=5``).

Each agent in the simulation has three characteristics: 

- age
- disease stage
- the time of their last exposure

For simplicity, let's assume we only consider three age groups: young (age 1-30), middle-aged (age 31-60), and elderly (age 61+). So, each agent's age can be one of these three categories. The disease stages we consider are susceptible (S), exposed (E), infected (I), recovered (R), and mortality (M). Initially, all agents are in the susceptible stage (no one is infected or exposed).

At each time step, agents can interact with each other, and their disease stages can change based on these interactions. The specific changes in disease stage are determined by two functions: 

- the transmission function: the transmission function calculates the probability of an agent getting infected based on their interactions with infected or exposed agents. Let's say the probability of infection transmission, calculated using a simplified formula, is 0.3. This means that there is a 30% chance of an interaction between a susceptible agent and an infected/exposed agent resulting in infection.

- the progression function: The progression function determines the transition from one disease stage to another over time. For example, let's assume that the transition from exposed (E) to infected (I) takes 2 time steps, the transition from infected (I) to recovered (R) takes 3 time steps, and the transition from infected (I) to mortality (M) takes 4 time steps. These transition times are fixed parameters in the simulation.

.. note::

    During each time step, agents interact with a set of neighboring agents, and their disease stages evolve accordingly. For example, let's say at time step 1, agent 1 interacts with agent 2, who is infected. Agent 1, being susceptible, has a 30% chance of getting infected based on the transmission function. If agent 1 gets infected, their disease stage changes from susceptible (S) to exposed (E).

    This process continues for all agents and time steps, with disease stage updates based on interactions and progression functions.

The simulation is parameterized with various time-dependent parameters, such as the disease reproduction number (measure of infection rate), age-specific susceptibility, stage-specific infection transmissibility, initial percentage of infections, stage transition times, and mortality rate. These parameters govern the behavior of the simulation over time.

Overall, this simplified example demonstrates how a discrete-event simulation can model the spread of a disease among a population of agents. The interactions between agents, their disease stages, and the probability of infection transmission are key factors in understanding and analyzing the dynamics of the simulated system.


Differentiable ABM
*******************

Certain assumptions that are commonly followed by epidemiologists. 
One important idea we use in this project is called GradABM, which uses a special type of calculation called differentiable sparse-tensor computation and 
takes into account the way the disease is transmitted.

Here are some real numbers to help explain the assumptions they make:

- It takes several days for an infection to develop after a person gets exposed to the disease.
- The decisions made by organizations like the CDC are based on forecasting and analysis done four weeks in advance.

Based on these assumptions, they make the following standard assumptions for their simulation:

- The simulation model divides time into days, so each step represents one day.
- On any given day, an infected person cannot infect others on the same day they got exposed.
- Once a person is infected, they cannot get reinfected while they are already infected.
- Once a person recovers or dies from the disease, they cannot get infected again. This assumption can be changed depending on the specific disease being studied.
- The cumulative effect of multiple interactions can lead to infection.

The above assumptions combined mean that the order of interactions within a day doesn't matter. 
This allows them to treat the interactions as interchangeable and makes the transmission model differentiable, 
which means it can be easily used in mathematical calculations.


.. note::

    Let's say we want to simulate the spread of a contagious disease within a small community of people. We can represent their social connections as a small-world graph, where each person is a node, and the connections between them are represented as edges.

    Imagine we have a community of 10 people, and they are connected in the following way:

    Person A is friends with B, C, and D.
    Person B is friends with A, C, and E.
    Person C is friends with A, B, D, and F.
    ...
    Person H is friends with E, I, and J.
    Person I is friends with G, H, and J.
    Person J is friends with H and I.

    This graph represents the social connections within the community. Now, let's say person A gets infected with the contagious disease. According to the assumptions made, the disease takes a few days to incubate before it becomes infectious.

    - On the first day, person A is exposed to the disease. They are not yet infectious, so they cannot transmit it to others.
    - On the second day, person A becomes infectious. They can now transmit the disease to their friends B, C, and D because they are connected in the small-world graph.
    - On the third day, person A has infected their friends B, C, and D. Now, B, C, and D become infectious and can potentially transmit the disease to their friends.

    This process continues for each infected person, spreading the disease through their social connections. 
    The simulation tracks the spread of the disease over time, based on the assumptions and the connections between individuals.

    Using sparse tensors as a mathematical representation helps with processing the large network of social connections efficiently. 
    It allows the simulation to handle a larger population, such as thousands or millions of people, 
    without becoming computationally expensive. 
    This improves the performance of the simulation and makes it easier to analyze the spread of the disease in realistic scenarios.
