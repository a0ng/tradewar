class AADDModel:
    def __init__(self):
        self.gdp = 100
        self.exchange_rate = 1.0
        self.current_account = 0
        
    def calculate_economic_state(self, state):
        """
        Calculate new economic state based on AA-DD model
        
        Args:
            state: dict containing:
                - tariff_rate: domestic tariff rate
                - foreign_tariff_rate: foreign tariff rate
                - world_demand: world demand percentage
                - domestic_demand: domestic demand percentage
                - retaliated: whether foreign countries just retaliated
                
        Returns:
            dict with new economic indicators:
                - gdp: new GDP level
                - exchange_rate: new exchange rate
                - current_account: new current account balance
        """
        # Effect of domestic tariff rate on GDP (DD curve)
        # Higher tariffs boost GDP by substituting imports with domestic production
        tariff_effect = (state['tariff_rate'] - 10) * 0.15

        # Effect of foreign tariffs on GDP (reduces exports)
        # Higher foreign tariffs hurt GDP by reducing exports
        foreign_tariff_effect = (state['foreign_tariff_rate'] - 10) * -0.12

        # Effect of world demand (DD curve)
        # Higher world demand increases exports and GDP
        world_demand_effect = (state['world_demand'] - 100) * 0.1

        # Effect of domestic demand (DD curve)
        # Higher domestic demand increases GDP
        domestic_demand_effect = (state['domestic_demand'] - 100) * 0.12

        # Calculate GDP change, including foreign tariff effects
        gdp_change = (
            tariff_effect +
            foreign_tariff_effect +
            world_demand_effect +
            domestic_demand_effect
        )
        self.gdp = max(50, min(150, self.gdp + gdp_change))

        # Effect of tariff rate on exchange rate (AA curve)
        # Higher domestic tariffs may appreciate the currency
        tariff_exchange_effect = (state['tariff_rate'] - 10) * 0.005

        # Effect of foreign tariff rate on exchange rate (AA curve)
        # Higher foreign tariffs may depreciate the domestic currency
        foreign_tariff_exchange_effect = (state['foreign_tariff_rate'] - 10) * -0.003

        # Current account affects exchange rate (AA curve)
        # A positive current account tends to appreciate the currency
        ca_exchange_effect = self.current_account * 0.01

        # Calculate exchange rate change, including foreign tariff effects
        exchange_rate_change = (
            tariff_exchange_effect +
            foreign_tariff_exchange_effect +
            ca_exchange_effect
        )
        self.exchange_rate = max(0.5, min(1.5, self.exchange_rate + exchange_rate_change))

        # Calculate current account based on tariffs, exchange rate, and demand
        tariff_ca_effect = (state['tariff_rate'] - 10) * 0.1
        foreign_tariff_ca_effect = (state['foreign_tariff_rate'] - 10) * -0.15
        exchange_rate_ca_effect = (1 - self.exchange_rate) * 8
        world_demand_ca_effect = (state['world_demand'] - 100) * 0.08
        domestic_demand_ca_effect = (100 - state['domestic_demand']) * 0.05

        # Calculate current account balance with foreign tariff effects
        self.current_account = max(-15, min(15,
            tariff_ca_effect +
            foreign_tariff_ca_effect +
            exchange_rate_ca_effect +
            world_demand_ca_effect +
            domestic_demand_ca_effect
        ))

        # If retaliation just happened this turn, add immediate extra impact
        if state['retaliated']:
            # Retaliation creates market uncertainty temporarily reducing GDP
            self.gdp -= 1.5
            # And can cause exchange rate volatility
            self.exchange_rate -= 0.02
            # And immediately worsens current account due to trade disruption
            self.current_account -= 0.8

        return {
            'gdp': self.gdp,
            'exchange_rate': self.exchange_rate,
            'current_account': self.current_account
        }

    def generate_aa_curve(self, state):
        """Generate points for AA curve"""
        points = []
        for gdp in range(60, 141, 5):
            # AA curve equation: Exchange rate = f(GDP, domestic tariff, foreign tariff)
            # Higher GDP tends to increase exchange rate in AA curve
            # Higher domestic tariffs tend to appreciate the exchange rate
            # Higher foreign tariffs tend to depreciate the exchange rate
            exchange_rate = (
                1 +
                (gdp - 100) * 0.002 +
                (state['tariff_rate'] - 10) * 0.005 +
                (state['foreign_tariff_rate'] - 10) * -0.003
            )
            points.append({'x': gdp, 'y': exchange_rate})
        return points

    def generate_dd_curve(self, state):
        """Generate points for DD curve"""
        points = []
        exchange_rate = 0.6
        while exchange_rate <= 1.4:
            # DD curve equation: GDP = f(Exchange rate, domestic tariff, foreign tariff)
            # Higher exchange rate reduces GDP in DD curve
            # Higher domestic tariffs increase GDP in DD curve
            # Higher foreign tariffs decrease GDP in DD curve
            gdp = (
                100 -
                (exchange_rate - 1) * 40 +
                (state['tariff_rate'] - 10) * 0.15 +
                (state['foreign_tariff_rate'] - 10) * -0.12
            )
            points.append({'x': gdp, 'y': exchange_rate})
            exchange_rate += 0.05
        return points

    def reset(self):
        """Reset the model to initial values"""
        self.gdp = 100
        self.exchange_rate = 1.0
        self.current_account = 0

    def calculate_gdp_change(self, state):
        """Calculate GDP change based on current state."""
        try:
            # Base GDP effects from tariffs
            tariff_effect = -0.2 * state.get('tariff_rate', 0)  # Negative effect from own tariffs
            foreign_tariff_effect = -0.3 * state.get('foreign_tariff_rate', 0)  # Stronger negative effect from foreign tariffs
            
            # Demand effects (normalized to percentage changes from baseline of 100)
            world_demand_effect = 0.3 * ((state.get('world_demand', 100) - 100) / 100)  # World demand above/below baseline
            domestic_demand_effect = 0.4 * ((state.get('domestic_demand', 100) - 100) / 100)  # Domestic demand above/below baseline
            
            # Calculate total policy effect
            policy_effect = tariff_effect + foreign_tariff_effect + world_demand_effect + domestic_demand_effect
            
            # Add natural growth (approximately 2% annually = 0.5% per quarter)
            natural_growth = 0.5
            
            # Apply retaliation penalty if applicable
            if state.get('retaliated', False):
                retaliation_penalty = -1.0  # 1% penalty for retaliation
            else:
                retaliation_penalty = 0
                
            # Calculate total GDP change
            total_gdp_change = policy_effect + natural_growth + retaliation_penalty
            
            # Ensure the change is within reasonable bounds (-5% to +5% per quarter)
            total_gdp_change = max(min(total_gdp_change, 5), -5)
            
            return total_gdp_change
            
        except Exception as e:
            print(f"Error in calculate_gdp_change: {str(e)}")
            return 0.5  # Return natural growth as fallback
