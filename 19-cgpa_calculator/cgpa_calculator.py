class CGPACalculator:
    def __init__(self):
        self.grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }
        self.semesters = []
    
    def validate_grade(self, grade):
        """Validate if the entered grade is valid"""
        return grade.upper() in self.grade_points
    
    def validate_credit_hours(self, credit_hours):
        """Validate credit hours"""
        try:
            credits = float(credit_hours)
            return credits > 0
        except ValueError:
            return False
    
    def calculate_semester_gpa(self, courses):
        """Calculate GPA for a single semester"""
        total_credit_hours = 0
        total_grade_points = 0
        
        for course in courses:
            grade = course['grade'].upper()
            credit_hours = course['credit_hours']
            
            grade_point = self.grade_points[grade]
            total_grade_points += grade_point * credit_hours
            total_credit_hours += credit_hours
        
        if total_credit_hours == 0:
            return 0.0
        
        return total_grade_points / total_credit_hours
    
    def calculate_cgpa(self):
        """Calculate overall CGPA across all semesters"""
        total_cumulative_credits = 0
        total_cumulative_grade_points = 0
        
        for semester in self.semesters:
            semester_gpa = semester['gpa']
            semester_credits = semester['total_credits']
            
            total_cumulative_grade_points += semester_gpa * semester_credits
            total_cumulative_credits += semester_credits
        
        if total_cumulative_credits == 0:
            return 0.0
        
        return total_cumulative_grade_points / total_cumulative_credits
    
    def add_semester(self, courses):
        """Add a semester with its courses"""
        semester_gpa = self.calculate_semester_gpa(courses)
        total_credits = sum(course['credit_hours'] for course in courses)
        
        semester_data = {
            'courses': courses,
            'gpa': semester_gpa,
            'total_credits': total_credits
        }
        
        self.semesters.append(semester_data)
        return semester_gpa
    
    def get_grade_summary(self):
        """Get summary of all grades across semesters"""
        summary = {}
        for semester in self.semesters:
            for course in semester['courses']:
                grade = course['grade'].upper()
                summary[grade] = summary.get(grade, 0) + 1
        return summary