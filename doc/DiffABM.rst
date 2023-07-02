
Methodology
=====


A discrete-event simulation
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

- the progression function: The progression function determines the transition from one disease stage to another over time. For simplicity, let's assume that the transition from exposed (E) to infected (I) takes 2 time steps, the transition from infected (I) to recovered (R) takes 3 time steps, and the transition from infected (I) to mortality (M) takes 4 time steps. These transition times are fixed parameters in the simulation.

.. note::

    During each time step, agents interact with a set of neighboring agents, and their disease stages evolve accordingly. For example, let's say at time step 1, agent 1 interacts with agent 2, who is infected. Agent 1, being susceptible, has a 30% chance of getting infected based on the transmission function. If agent 1 gets infected, their disease stage changes from susceptible (S) to exposed (E).

    This process continues for all agents and time steps, with disease stage updates based on interactions and progression functions.

The simulation is parameterized with various time-dependent parameters, such as the disease reproduction number (measure of infection rate), age-specific susceptibility, stage-specific infection transmissibility, initial percentage of infections, stage transition times, and mortality rate. These parameters govern the behavior of the simulation over time.

Overall, this simplified example demonstrates how a discrete-event simulation can model the spread of a disease among a population of agents. The interactions between agents, their disease stages, and the probability of infection transmission are key factors in understanding and analyzing the dynamics of the simulated system.