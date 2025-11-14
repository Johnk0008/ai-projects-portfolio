from cgpa_calculator import CGPACalculator
import os

class CGPAApplication:
    def __init__(self):
        self.calculator = CGPACalculator()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display application header"""
        print("=" * 60)
        print("           ADVANCED CGPA CALCULATOR")
        print("=" * 60)
        print()
    
    def get_course_input(self, course_number):
        """Get input for a single course"""
        print(f"\n--- Course {course_number} ---")
        
        while True:
            grade = input("Enter grade (A+, A, A-, B+, B, B-, C+, C, C-, D+, D, F): ").strip().upper()
            if self.calculator.validate_grade(grade):
                break
            print("❌ Invalid grade! Please enter a valid grade.")
        
        while True:
            credit_hours = input("Enter credit hours: ").strip()
            if self.calculator.validate_credit_hours(credit_hours):
                credit_hours = float(credit_hours)
                break
            print("❌ Invalid credit hours! Please enter a positive number.")
        
        return {
            'name': f"Course {course_number}",
            'grade': grade,
            'credit_hours': credit_hours
        }
    
    def input_semester_data(self):
        """Input data for a single semester"""
        self.clear_screen()
        self.display_header()
        print("📚 SEMESTER DATA ENTRY")
        print("-" * 40)
        
        while True:
            try:
                num_courses = int(input("\nEnter number of courses in this semester: "))
                if num_courses > 0:
                    break
                print("❌ Please enter a positive number!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        courses = []
        for i in range(1, num_courses + 1):
            course = self.get_course_input(i)
            courses.append(course)
        
        return courses
    
    def display_semester_results(self, semester_number, semester_gpa, courses):
        """Display results for a single semester"""
        self.clear_screen()
        self.display_header()
        print(f"🎓 SEMESTER {semester_number} RESULTS")
        print("-" * 50)
        
        print("\n📊 COURSE DETAILS:")
        print("-" * 30)
        print(f"{'Course':<10} {'Grade':<8} {'Credits':<10} {'Grade Points':<12}")
        print("-" * 50)
        
        for i, course in enumerate(courses, 1):
            grade_point = self.calculator.grade_points[course['grade'].upper()]
            points_earned = grade_point * course['credit_hours']
            print(f"{f'Course {i}':<10} {course['grade']:<8} {course['credit_hours']:<10.1f} {points_earned:<12.2f}")
        
        print("-" * 50)
        total_credits = sum(course['credit_hours'] for course in courses)
        print(f"{'TOTAL':<10} {'':<8} {total_credits:<10.1f} {'':<12}")
        
        print(f"\n✅ Semester GPA: {semester_gpa:.3f}")
        
        # Grade interpretation
        if semester_gpa >= 3.7:
            interpretation = "Excellent! First Class"
        elif semester_gpa >= 3.3:
            interpretation = "Very Good!"
        elif semester_gpa >= 3.0:
            interpretation = "Good!"
        elif semester_gpa >= 2.0:
            interpretation = "Satisfactory"
        else:
            interpretation = "Needs Improvement"
        
        print(f"📈 Performance: {interpretation}")
    
    def display_final_results(self):
        """Display final CGPA and summary"""
        self.clear_screen()
        self.display_header()
        print("🎯 FINAL ACADEMIC SUMMARY")
        print("=" * 50)
        
        print(f"\n📅 Total Semesters Completed: {len(self.calculator.semesters)}")
        
        # Display semester-wise GPA
        print("\n📊 SEMESTER-WISE PERFORMANCE:")
        print("-" * 30)
        for i, semester in enumerate(self.calculator.semesters, 1):
            print(f"Semester {i}: GPA = {semester['gpa']:.3f}, Credits = {semester['total_credits']}")
        
        # Calculate and display CGPA
        cgpa = self.calculator.calculate_cgpa()
        print(f"\n🏆 OVERALL CGPA: {cgpa:.3f}")
        
        # CGPA interpretation
        if cgpa >= 3.7:
            classification = "First Class with Distinction"
        elif cgpa >= 3.3:
            classification = "First Class"
        elif cgpa >= 3.0:
            classification = "Second Class Upper"
        elif cgpa >= 2.0:
            classification = "Second Class Lower"
        else:
            classification = "Needs Improvement"
        
        print(f"🎓 Classification: {classification}")
        
        # Grade distribution
        grade_summary = self.calculator.get_grade_summary()
        if grade_summary:
            print("\n📈 GRADE DISTRIBUTION:")
            print("-" * 20)
            for grade, count in sorted(grade_summary.items()):
                print(f"{grade}: {count} courses")
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.display_header()
            print("1. 📝 Add New Semester Data")
            print("2. 🎯 Calculate Final CGPA")
            print("3. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                courses = self.input_semester_data()
                semester_gpa = self.calculator.add_semester(courses)
                self.display_semester_results(len(self.calculator.semesters), semester_gpa, courses)
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                if not self.calculator.semesters:
                    print("\n❌ No semester data available! Please add semester data first.")
                    input("Press Enter to continue...")
                else:
                    self.display_final_results()
                    input("\nPress Enter to continue...")
            
            elif choice == '3':
                print("\n👋 Thank you for using the CGPA Calculator!")
                break
            
            else:
                print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
                input("Press Enter to continue...")

def main():
    app = CGPAApplication()
    app.run()

if __name__ == "__main__":
    main()