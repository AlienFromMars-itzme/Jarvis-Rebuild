"""Calculator module for Jarvis AI Assistant."""

import re
from typing import Optional, Union


class Calculator:
    """Voice-activated calculator."""
    
    def __init__(self):
        """Initialize calculator."""
        pass
    
    def evaluate_expression(self, expression: str) -> Optional[Union[int, float]]:
        """Safely evaluate a mathematical expression."""
        try:
            # Remove any non-mathematical characters
            expression = expression.strip()
            
            # Replace common spoken words with operators
            replacements = {
                ' plus ': '+',
                ' add ': '+',
                ' minus ': '-',
                ' subtract ': '-',
                ' times ': '*',
                ' multiply ': '*',
                ' multiplied by ': '*',
                ' divided by ': '/',
                ' divide ': '/',
                ' power ': '**',
                ' to the power of ': '**',
                ' squared': '**2',
                ' cubed': '**3',
                ' percent': '/100',
                ' percentage': '/100'
            }
            
            expr_lower = expression.lower()
            for word, operator in replacements.items():
                expr_lower = expr_lower.replace(word, operator)
            
            # Remove spaces
            expr_lower = expr_lower.replace(' ', '')
            
            # Only allow safe characters
            if not re.match(r'^[0-9+\-*/().]+$', expr_lower):
                return None
            
            # Evaluate safely
            result = eval(expr_lower, {"__builtins__": {}}, {})
            
            return result
        except Exception as e:
            print(f"Calculation error: {e}")
            return None
    
    def parse_calculation(self, text: str) -> Optional[str]:
        """Parse and calculate from voice input."""
        text = text.lower().strip()
        
        # Remove common prefixes
        prefixes = ['calculate', 'compute', 'what is', 'what\'s', 'solve']
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break
        
        result = self.evaluate_expression(text)
        
        if result is not None:
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 2)
            return str(result)
        
        return None
    
    def convert_units(self, value: float, from_unit: str, to_unit: str) -> Optional[float]:
        """Convert between units."""
        conversions = {
            # Length
            ('meter', 'kilometer'): 0.001,
            ('meter', 'centimeter'): 100,
            ('meter', 'millimeter'): 1000,
            ('meter', 'mile'): 0.000621371,
            ('meter', 'yard'): 1.09361,
            ('meter', 'foot'): 3.28084,
            ('meter', 'inch'): 39.3701,
            ('kilometer', 'meter'): 1000,
            ('kilometer', 'mile'): 0.621371,
            ('mile', 'kilometer'): 1.60934,
            ('mile', 'meter'): 1609.34,
            ('foot', 'meter'): 0.3048,
            ('foot', 'inch'): 12,
            ('inch', 'centimeter'): 2.54,
            
            # Weight
            ('kilogram', 'gram'): 1000,
            ('kilogram', 'pound'): 2.20462,
            ('kilogram', 'ounce'): 35.274,
            ('gram', 'kilogram'): 0.001,
            ('pound', 'kilogram'): 0.453592,
            ('pound', 'ounce'): 16,
            ('ounce', 'gram'): 28.3495,
            
            # Temperature (requires special handling)
            # Volume
            ('liter', 'milliliter'): 1000,
            ('liter', 'gallon'): 0.264172,
            ('gallon', 'liter'): 3.78541,
        }
        
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Check if conversion exists
        if (from_unit, to_unit) in conversions:
            return value * conversions[(from_unit, to_unit)]
        
        # Check reverse
        if (to_unit, from_unit) in conversions:
            return value / conversions[(to_unit, from_unit)]
        
        # Special handling for temperature
        if from_unit == 'celsius':
            if to_unit == 'fahrenheit':
                return (value * 9/5) + 32
            elif to_unit == 'kelvin':
                return value + 273.15
        elif from_unit == 'fahrenheit':
            if to_unit == 'celsius':
                return (value - 32) * 5/9
            elif to_unit == 'kelvin':
                return (value - 32) * 5/9 + 273.15
        elif from_unit == 'kelvin':
            if to_unit == 'celsius':
                return value - 273.15
            elif to_unit == 'fahrenheit':
                return (value - 273.15) * 9/5 + 32
        
        return None


# Global calculator instance
calculator = Calculator()
