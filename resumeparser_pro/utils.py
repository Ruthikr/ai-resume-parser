"""
Utility functions for resume parsing
"""

import re
from typing import Dict, List, Any
from datetime import datetime
from dateutil import parser as date_parser

try:
    import phonenumbers
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

class PostProcessor:
    """Post-processing utilities for parsed resume data"""
    
    @staticmethod
    def clean_contact_info(contact: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate contact information"""
        # Clean email validation
        if contact.get('email'):
            email = contact['email']
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                contact['email'] = None
        
        # Extract URLs from other_profiles
        profiles = contact.get('other_profiles', [])
        for profile in profiles:
            profile_lower = profile.lower()
            if 'linkedin' in profile_lower and not contact.get('linkedin'):
                contact['linkedin'] = profile if profile.startswith(('http://', 'https://')) else f'https://{profile}'
            if 'github' in profile_lower and not contact.get('github'):
                contact['github'] = profile if profile.startswith(('http://', 'https://')) else f'https://{profile}'
        
        # Phone number formatting
        if contact.get('phone') and PHONENUMBERS_AVAILABLE:
            try:
                phone_raw = contact['phone']
                cleaned_phone = re.sub(r'[^\d+\-\s\(\)]', '', phone_raw)
                contact['phone'] = cleaned_phone
                
                try:
                    phone_obj = phonenumbers.parse(phone_raw, 'US')
                    if phonenumbers.is_valid_number(phone_obj):
                        contact['phone'] = phonenumbers.format_number(phone_obj, phonenumbers.PhoneNumberFormat.E164)
                except:
                    pass
            except Exception:
                pass
        
        # Validate URLs
        url_fields = ['linkedin', 'github', 'portfolio']
        for field in url_fields:
            if contact.get(field):
                url = contact[field]
                if not (url.startswith('http://') or url.startswith('https://')):
                    contact[field] = f"https://{url}"
        
        return contact
    
    @staticmethod
    def calculate_duration_months(experiences: List[Dict]) -> int:
        """Calculate total experience in months"""
        total_months = 0
        
        for exp in experiences:
            try:
                duration_months = exp.get('duration_months')
                if duration_months and isinstance(duration_months, int):
                    total_months += duration_months
                else:
                    # Fallback calculation
                    start = exp.get('start_date', '')
                    end = exp.get('end_date', '')
                    
                    if start and end:
                        if end.lower() == 'present':
                            end = datetime.now().strftime('%Y-%m')
                        
                        start_dt = date_parser.parse(start, fuzzy=True)
                        end_dt = date_parser.parse(end, fuzzy=True)
                        
                        months = (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month)
                        total_months += max(1, months)
            
            except (ValueError, TypeError):
                continue
        
        return total_months
    
    @staticmethod
    def standardize_gpa(gpa_str: str) -> str:
        """Standardize GPA format"""
        if not gpa_str:
            return gpa_str
        
        try:
            gpa_clean = gpa_str.strip().lower()
            # Look for decimal GPA
            match = re.search(r'(\d\.\d{1,3})', gpa_clean)
            if match:
                return match.group(1)
            else:
                # Look for percentage
                match_pct = re.search(r'(\d{1,3})%', gpa_clean)
                if match_pct:
                    percentage = float(match_pct.group(1))
                    gpa_decimal = round(percentage / 25.0, 2)
                    return str(gpa_decimal)
        except Exception:
            pass
        
        return gpa_str
