import random
import time

class System:
    def __init__(self, name="Generic System"):
        self.name = name
        self.cpu_usage = 20  # % initial
        self.memory_usage = 30 # % initial
        self.network_io = 10 # MB/s initial
        self.internal_corruption_level = 0 # 0-100, this is the 'unknown' or unmonitored factor
        self.operational_cycles = 0

        # Define "normal" ranges for *monitored* metrics
        self.NORMAL_CPU_RANGE = (10, 70)
        self.NORMAL_MEMORY_RANGE = (20, 80)
        self.NORMAL_NETWORK_RANGE = (5, 50)

        # Thresholds for internal corruption (the 'pathological' state from Canguilhem's view)
        self.CRITICAL_CORRUPTION_THRESHOLD = 70
        self.STRESS_CORRUPTION_THRESHOLD = 30

    def _adjust_monitored_metrics(self):
        # Simulate normal fluctuations in monitored metrics
        self.cpu_usage = max(0, min(100, self.cpu_usage + random.uniform(-5, 5)))
        self.memory_usage = max(0, min(100, self.memory_usage + random.uniform(-3, 3)))
        self.network_io = max(0, min(100, self.network_io + random.uniform(-2, 2)))

        # Canguilhem's "Normativity": The system actively tries to maintain its function
        # and perceived 'normal' state even as internal issues arise. It compensates.
        # As internal corruption grows, the system might use more resources
        # to keep performance stable, pushing monitored metrics towards the higher end of "normal".
        if self.internal_corruption_level > self.STRESS_CORRUPTION_THRESHOLD:
            # System works harder to appear normal, consuming more resources
            self.cpu_usage = min(self.NORMAL_CPU_RANGE[1] - 5, self.cpu_usage + random.uniform(1, 3))
            self.memory_usage = min(self.NORMAL_MEMORY_RANGE[1] - 5, self.memory_usage + random.uniform(0.5, 1.5))

    def simulate_cycle(self):
        self.operational_cycles += 1
        # Simulate internal corruption increasing over time (the 'unknown' factor)
        self.internal_corruption_level = min(100, self.internal_corruption_level + random.uniform(1, 5))

        self._adjust_monitored_metrics()

    def get_monitored_status(self):
        return {
            "cpu_usage": round(self.cpu_usage, 2),
            "memory_usage": round(self.memory_usage, 2),
            "network_io": round(self.network_io, 2)
        }

    def is_monitored_normal(self):
        # Checks if the system appears "normal" based *only* on the monitored metrics
        cpu_ok = self.NORMAL_CPU_RANGE[0] <= self.cpu_usage <= self.NORMAL_CPU_RANGE[1]
        mem_ok = self.NORMAL_MEMORY_RANGE[0] <= self.memory_usage <= self.NORMAL_MEMORY_RANGE[1]
        net_ok = self.NORMAL_NETWORK_RANGE[0] <= self.network_io <= self.NORMAL_NETWORK_RANGE[1]
        return cpu_ok and mem_ok and net_ok

    def is_truly_healthy(self):
        # Checks if the system is *truly* healthy, considering the 'unknown' internal state.
        # This reflects Canguilhem's idea that 'normal' isn't just statistical conformity,
        # but an active capacity to function well and adapt without critical internal degradation.
        return self.internal_corruption_level < self.CRITICAL_CORRUPTION_THRESHOLD

    def __str__(self):
        status = self.get_monitored_status()
        monitored_normal = self.is_monitored_normal()
        truly_healthy = self.is_truly_healthy()

        output = f"--- {self.name} - Cycle {self.operational_cycles} ---\n"
        output += f"  Monitored Metrics: CPU={status['cpu_usage']}%, Mem={status['memory_usage']}%, Net={status['network_io']}MB/s\n"
        output += f"  Monitored Status: {'NORMAL' if monitored_normal else 'ABNORMAL'} (based on known metrics)\n"
        output += f"  Internal Corruption (UNKNOWN to standard monitoring): {round(self.internal_corruption_level, 2)}%\n"
        output += f"  True Health Status: {'HEALTHY' if truly_healthy else 'CRITICAL'} (considering internal state)\n"
        return output

# --- Simulation --- 
if __name__ == "__main__":
    system = System("Dev.to Blog Server")
    print("Simulating a system over time, demonstrating Canguilhem's 'Normal' and the 'Unknown'.\n")
    print("Initial State:")
    print(system)
    print("-" * 40)
    time.sleep(1)

    for i in range(1, 15): # Simulate 15 operational cycles
        system.simulate_cycle()
        print(system)

        # Highlight the discrepancy between monitored 'normal' and true health
        if system.is_monitored_normal() and not system.is_truly_healthy():
            print("!!! WARNING: System appears NORMAL by monitoring, but is CRITICALLY UNHEALTHY internally! (The 'Unknown' problem)")
            # This state exemplifies Canguilhem's concept: the system is still 'normative'
            # trying to maintain its function, but its internal capacity is degraded.
        elif not system.is_monitored_normal() and system.is_truly_healthy():
            print("!!! NOTE: System appears ABNORMAL by monitoring, but is still TRULY HEALTHY internally. (Temporary anomaly)")
        elif not system.is_monitored_normal() and not system.is_truly_healthy():
            print("!!! CRITICAL: System is ABNORMAL by monitoring AND CRITICALLY UNHEALTHY internally. (Failure imminent)")
        print("-" * 40)
        time.sleep(1)

    print("\nSimulation Finished.")
    print("This example illustrates how a system can appear 'normal' based on observed metrics,")
    print("while an unmonitored 'unknown' factor degrades its true health, aligning with")
    print("Canguilhem's view that 'normal' is not just statistical conformity but an active capacity.")
