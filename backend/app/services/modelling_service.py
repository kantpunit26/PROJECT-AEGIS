import math
from typing import Dict, Any, List
from app.schemas.modelling import SEIRParameters, SEIRSimulationResult

class EpidemiologicalModellingService:
    """
    Independent deterministic differential equation solver for hospital-associated
    bacterial transmission, asymptomatic colonization (C), symptomatic infection (I),
    antibiotic exposure (delta), and decolonization.
    """

    @staticmethod
    def simulate_seir_extended(params: SEIRParameters) -> SEIRSimulationResult:
        """
        Solves the extended Susceptible-Colonized-Infected-Recovered (SCIR) ODE system:
        dS/dt = Lambda - beta * S * (I + theta * C)/N - mu * S
        dC/dt = beta * S * (I + theta * C)/N - (alpha + gamma_c + mu) * C + delta * I
        dI/dt = alpha * C - (gamma_i + delta + mu + d) * I
        dR/dt = gamma_c * C + gamma_i * I - mu * R
        """
        N = params.total_population
        dt = params.time_step
        total_steps = int(params.simulation_days / dt)

        # Baseline Parameters
        beta = params.beta_transmission
        theta = params.theta_carrier_infectivity
        alpha = params.alpha_progression
        gamma_c = params.gamma_colonized_clearance
        gamma_i = params.gamma_infection_clearance
        delta = params.delta_treatment_exposure
        mu = params.natural_mortality_mu
        d = params.disease_induced_mortality
        Lambda = mu * N  # Balanced demographic inflow

        # Calculate Basic Reproduction Number R0 using the Next-Generation Matrix method
        # Transmission from colonized state + Progression to infected state
        term_colonized = (beta * theta) / (alpha + gamma_c + mu)
        term_infected = (beta * alpha) / ((alpha + gamma_c + mu) * (gamma_i + delta + mu + d))
        r0 = round(term_colonized + term_infected, 3)

        # Initial state vectors
        S = params.initial_susceptible
        C = params.initial_colonized
        I = params.initial_infected
        R = params.initial_recovered

        time_points = []
        s_arr = []
        c_arr = []
        i_arr = []
        r_arr = []
        re_arr = []

        peak_i = I
        peak_day = 0
        total_incidence = 0.0

        def derivatives(s_val: float, c_val: float, i_val: float, r_val: float):
            force = beta * (i_val + theta * c_val) / N
            ds = Lambda - force * s_val - mu * s_val
            dc = force * s_val - (alpha + gamma_c + mu) * c_val + delta * i_val
            di = alpha * c_val - (gamma_i + delta + mu + d) * i_val
            dr = gamma_c * c_val + gamma_i * i_val - mu * r_val
            return ds, dc, di, dr

        current_t = 0.0
        for step in range(total_steps):
            if step % int(1.0 / dt) == 0:
                day_int = int(round(current_t))
                time_points.append(round(current_t, 1))
                s_arr.append(round(S, 2))
                c_arr.append(round(C, 2))
                i_arr.append(round(I, 2))
                r_arr.append(round(R, 2))
                
                # Effective reproduction number Re = R0 * (S / N)
                re = round(r0 * (S / N), 3)
                re_arr.append(re)

                if I > peak_i:
                    peak_i = I
                    peak_day = day_int

            # 4th Order Runge-Kutta (RK4) Integration Step
            k1_s, k1_c, k1_i, k1_r = derivatives(S, C, I, R)
            
            k2_s, k2_c, k2_i, k2_r = derivatives(
                S + 0.5 * dt * k1_s,
                C + 0.5 * dt * k1_c,
                I + 0.5 * dt * k1_i,
                R + 0.5 * dt * k1_r
            )
            
            k3_s, k3_c, k3_i, k3_r = derivatives(
                S + 0.5 * dt * k2_s,
                C + 0.5 * dt * k2_c,
                I + 0.5 * dt * k2_i,
                R + 0.5 * dt * k2_r
            )
            
            k4_s, k4_c, k4_i, k4_r = derivatives(
                S + dt * k3_s,
                C + dt * k3_c,
                I + dt * k3_i,
                R + dt * k3_r
            )

            # Update compartments
            dS = (dt / 6.0) * (k1_s + 2 * k2_s + 2 * k3_s + k4_s)
            dC = (dt / 6.0) * (k1_c + 2 * k2_c + 2 * k3_c + k4_c)
            dI = (dt / 6.0) * (k1_i + 2 * k2_i + 2 * k3_i + k4_i)
            dR = (dt / 6.0) * (k1_r + 2 * k2_r + 2 * k3_r + k4_r)

            # Track new colonizations
            new_colonized = max(0.0, beta * (I + theta * C) * (S / N) * dt)
            total_incidence += new_colonized

            S = max(0.0, S + dS)
            C = max(0.0, C + dC)
            I = max(0.0, I + dI)
            R = max(0.0, R + dR)
            current_t += dt

        return SEIRSimulationResult(
            days=time_points,
            susceptible=s_arr,
            colonized=c_arr,
            infected=i_arr,
            recovered=r_arr,
            r0=r0,
            effective_re=re_arr,
            peak_infected_count=round(peak_i, 2),
            peak_day=peak_day,
            total_colonization_incidence=round(total_incidence, 1)
        )

modelling_service = EpidemiologicalModellingService()
