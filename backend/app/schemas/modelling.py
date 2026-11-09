from typing import Optional, List, Dict
from datetime import datetime
from pydantic import BaseModel, Field

class SEIRParameters(BaseModel):
    total_population: float = Field(default=1000.0, description="Total hospital or regional susceptible population N")
    initial_susceptible: float = Field(default=990.0)
    initial_colonized: float = Field(default=8.0, description="Asymptomatic colonized carriers C")
    initial_infected: float = Field(default=2.0, description="Symptomatic active clinical infections I")
    initial_recovered: float = Field(default=0.0)
    
    beta_transmission: float = Field(default=0.28, description="Transmission rate parameter beta")
    theta_carrier_infectivity: float = Field(default=0.35, description="Relative infectivity of colonized carriers theta")
    alpha_progression: float = Field(default=0.08, description="Rate of progression from colonization to active infection alpha")
    gamma_colonized_clearance: float = Field(default=0.03, description="Spontaneous carrier decolonization rate gamma_c")
    gamma_infection_clearance: float = Field(default=0.10, description="Infection recovery / clearance rate gamma_i")
    delta_treatment_exposure: float = Field(default=0.05, description="Rate of antimicrobial therapy effect / de-escalation delta")
    natural_mortality_mu: float = Field(default=0.002)
    disease_induced_mortality: float = Field(default=0.015)
    
    simulation_days: int = Field(default=120, description="Simulation duration in days")
    time_step: float = Field(default=0.5, description="Numerical integration step dt")

class SEIRSimulationResult(BaseModel):
    days: List[float]
    susceptible: List[float]
    colonized: List[float]
    infected: List[float]
    recovered: List[float]
    r0: float
    effective_re: List[float]
    peak_infected_count: float
    peak_day: int
    total_colonization_incidence: float

