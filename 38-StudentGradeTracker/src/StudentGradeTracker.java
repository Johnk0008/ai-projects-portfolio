import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.Scanner;

public class StudentGradeTracker {
    private ArrayList<Student> students;
    private Scanner scanner;

    public StudentGradeTracker() {
        students = new ArrayList<>();
        scanner = new Scanner(System.in);
    }

    // Student class to store student information
    class Student {
        private String name;
        private int id;
        private ArrayList<Double> grades;

        public Student(String name, int id) {
            this.name = name;
            this.id = id;
            this.grades = new ArrayList<>();
        }

        public void addGrade(double grade) {
            if (grade >= 0 && grade <= 100) {
                grades.add(grade);
            } else {
                System.out.println("Warning: Grade " + grade + " is outside typical range (0-100)");
                grades.add(grade); // Still add it but warn the user
            }
        }

        public double calculateAverage() {
            if (grades.isEmpty()) return 0.0;
            double sum = 0;
            for (double grade : grades) {
                sum += grade;
            }
            return sum / grades.size();
        }

        public double getHighestGrade() {
            if (grades.isEmpty()) return 0.0;
            double highest = grades.get(0);
            for (double grade : grades) {
                if (grade > highest) highest = grade;
            }
            return highest;
        }

        public double getLowestGrade() {
            if (grades.isEmpty()) return 0.0;
            double lowest = grades.get(0);
            for (double grade : grades) {
                if (grade < lowest) lowest = grade;
            }
            return lowest;
        }

        public String getName() { return name; }
        public int getId() { return id; }
        public ArrayList<Double> getGrades() { return grades; }
        
        public String getGradeLetter(double grade) {
            if (grade >= 90) return "A";
            else if (grade >= 80) return "B";
            else if (grade >= 70) return "C";
            else if (grade >= 60) return "D";
            else return "F";
        }
    }

    // Helper method to get valid integer input
    private int getValidIntInput(String prompt) {
        while (true) {
            try {
                System.out.print(prompt);
                int value = scanner.nextInt();
                scanner.nextLine(); // consume newline
                return value;
            } catch (InputMismatchException e) {
                System.out.println("Invalid input! Please enter a valid integer.");
                scanner.nextLine(); // clear invalid input
            }
        }
    }

    // Helper method to get valid double input
    private double getValidDoubleInput(String prompt) {
        while (true) {
            try {
                System.out.print(prompt);
                double value = scanner.nextDouble();
                scanner.nextLine(); // consume newline
                return value;
            } catch (InputMismatchException e) {
                System.out.println("Invalid input! Please enter a valid number.");
                scanner.nextLine(); // clear invalid input
            }
        }
    }

    // Helper method to convert letter grade to numeric value
    private double convertLetterGrade(String letterGrade) {
        switch (letterGrade.toUpperCase()) {
            case "A+": return 97.0;
            case "A": return 93.0;
            case "A-": return 90.0;
            case "B+": return 87.0;
            case "B": return 83.0;
            case "B-": return 80.0;
            case "C+": return 77.0;
            case "C": return 73.0;
            case "C-": return 70.0;
            case "D+": return 67.0;
            case "D": return 63.0;
            case "D-": return 60.0;
            case "F": return 50.0;
            default: return -1; // Invalid grade
        }
    }

    // Method to get grade input (supports both numeric and letter grades)
    private double getGradeInput() {
        while (true) {
            System.out.print("Enter grade (numeric 0-100 or letter grade A-F): ");
            String input = scanner.nextLine().trim();
            
            try {
                // Try to parse as numeric grade
                double numericGrade = Double.parseDouble(input);
                return numericGrade;
            } catch (NumberFormatException e) {
                // If not numeric, try to convert letter grade
                double convertedGrade = convertLetterGrade(input);
                if (convertedGrade != -1) {
                    System.out.println("Converted '" + input + "' to numeric value: " + convertedGrade);
                    return convertedGrade;
                } else {
                    System.out.println("Invalid grade! Please enter a number (0-100) or valid letter grade (A-F).");
                }
            }
        }
    }

    public void addStudent() {
        System.out.print("Enter student name: ");
        String name = scanner.nextLine();
        
        int id = getValidIntInput("Enter student ID: ");

        // Check if student ID already exists
        if (findStudentById(id) != null) {
            System.out.println("Student with ID " + id + " already exists!");
            return;
        }

        Student student = new Student(name, id);
        students.add(student);
        System.out.println("Student '" + name + "' added successfully!");
    }

    public void addGradesToStudent() {
        if (students.isEmpty()) {
            System.out.println("No students available. Please add students first.");
            return;
        }

        displayStudents();
        int id = getValidIntInput("Enter student ID to add grades: ");

        Student student = findStudentById(id);
        if (student != null) {
            double grade = getGradeInput();
            student.addGrade(grade);
            System.out.println("Grade " + grade + " added successfully to " + student.getName() + "!");
            System.out.println("Letter grade: " + student.getGradeLetter(grade));
        } else {
            System.out.println("Student with ID " + id + " not found!");
        }
    }

    public void displayStudents() {
        if (students.isEmpty()) {
            System.out.println("No students available.");
            return;
        }

        System.out.println("\n=== Student List ===");
        for (Student student : students) {
            System.out.println("ID: " + student.getId() + ", Name: " + student.getName());
        }
    }

    public void displayStudentDetails() {
        if (students.isEmpty()) {
            System.out.println("No students available.");
            return;
        }

        int id = getValidIntInput("Enter student ID to view details: ");
        Student student = findStudentById(id);
        
        if (student != null) {
            System.out.println("\n=== STUDENT DETAILS ===");
            System.out.println("ID: " + student.getId());
            System.out.println("Name: " + student.getName());
            System.out.println("Grades: " + student.getGrades());
            
            if (!student.getGrades().isEmpty()) {
                System.out.println("Average: " + String.format("%.2f", student.calculateAverage()));
                System.out.println("Highest: " + student.getHighestGrade());
                System.out.println("Lowest: " + student.getLowestGrade());
                System.out.println("Letter Grade Average: " + student.getGradeLetter(student.calculateAverage()));
            } else {
                System.out.println("No grades available for this student.");
            }
        } else {
            System.out.println("Student not found!");
        }
    }

    public void displaySummaryReport() {
        if (students.isEmpty()) {
            System.out.println("No students available.");
            return;
        }

        System.out.println("\n=== STUDENT GRADE SUMMARY REPORT ===");
        System.out.println("==================================================================================");
        System.out.printf("%-10s %-20s %-10s %-10s %-10s %-10s%n", 
                         "ID", "Name", "Average", "Letter", "Highest", "Lowest");
        System.out.println("==================================================================================");

        for (Student student : students) {
            double average = student.calculateAverage();
            System.out.printf("%-10d %-20s %-10.2f %-10s %-10.2f %-10.2f%n",
                            student.getId(),
                            student.getName(),
                            average,
                            student.getGradeLetter(average),
                            student.getHighestGrade(),
                            student.getLowestGrade());
        }

        // Overall statistics
        displayOverallStatistics();
    }

    private void displayOverallStatistics() {
        System.out.println("\n=== OVERALL STATISTICS ===");
        System.out.printf("Total Students: %d%n", students.size());
        
        if (!students.isEmpty()) {
            System.out.printf("Class Average: %.2f%n", calculateClassAverage());
            System.out.printf("Overall Highest Grade: %.2f%n", getOverallHighestGrade());
            System.out.printf("Overall Lowest Grade: %.2f%n", getOverallLowestGrade());
            
            // Grade distribution
            int aCount = 0, bCount = 0, cCount = 0, dCount = 0, fCount = 0;
            for (Student student : students) {
                if (!student.getGrades().isEmpty()) {
                    String letterGrade = student.getGradeLetter(student.calculateAverage());
                    switch (letterGrade) {
                        case "A": aCount++; break;
                        case "B": bCount++; break;
                        case "C": cCount++; break;
                        case "D": dCount++; break;
                        case "F": fCount++; break;
                    }
                }
            }
            
            System.out.println("\n=== GRADE DISTRIBUTION ===");
            System.out.println("A: " + aCount + " students");
            System.out.println("B: " + bCount + " students");
            System.out.println("C: " + cCount + " students");
            System.out.println("D: " + dCount + " students");
            System.out.println("F: " + fCount + " students");
        }
    }

    private double calculateClassAverage() {
        if (students.isEmpty()) return 0.0;
        double total = 0;
        int count = 0;
        for (Student student : students) {
            if (!student.getGrades().isEmpty()) {
                total += student.calculateAverage();
                count++;
            }
        }
        return count > 0 ? total / count : 0.0;
    }

    private double getOverallHighestGrade() {
        if (students.isEmpty()) return 0.0;
        double highest = Double.MIN_VALUE;
        for (Student student : students) {
            if (!student.getGrades().isEmpty()) {
                double studentHighest = student.getHighestGrade();
                if (studentHighest > highest) highest = studentHighest;
            }
        }
        return highest != Double.MIN_VALUE ? highest : 0.0;
    }

    private double getOverallLowestGrade() {
        if (students.isEmpty()) return 0.0;
        double lowest = Double.MAX_VALUE;
        for (Student student : students) {
            if (!student.getGrades().isEmpty()) {
                double studentLowest = student.getLowestGrade();
                if (studentLowest < lowest) lowest = studentLowest;
            }
        }
        return lowest != Double.MAX_VALUE ? lowest : 0.0;
    }

    private Student findStudentById(int id) {
        for (Student student : students) {
            if (student.getId() == id) {
                return student;
            }
        }
        return null;
    }

    public void displayMenu() {
        System.out.println("\n=== STUDENT GRADE TRACKER ===");
        System.out.println("1. Add Student");
        System.out.println("2. Add Grades to Student");
        System.out.println("3. Display All Students");
        System.out.println("4. Display Student Details");
        System.out.println("5. Display Summary Report");
        System.out.println("6. Exit");
        System.out.print("Choose an option (1-6): ");
    }

    public void run() {
        System.out.println("Welcome to Student Grade Tracker!");
        System.out.println("Now supporting both numeric and letter grades!");
        
        int choice;
        do {
            try {
                displayMenu();
                choice = scanner.nextInt();
                scanner.nextLine(); // consume newline

                switch (choice) {
                    case 1:
                        addStudent();
                        break;
                    case 2:
                        addGradesToStudent();
                        break;
                    case 3:
                        displayStudents();
                        break;
                    case 4:
                        displayStudentDetails();
                        break;
                    case 5:
                        displaySummaryReport();
                        break;
                    case 6:
                        System.out.println("Thank you for using Student Grade Tracker!");
                        break;
                    default:
                        System.out.println("Invalid option! Please choose 1-6.");
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input! Please enter a number between 1-6.");
                scanner.nextLine(); // clear invalid input
                choice = 0;
            }
        } while (choice != 6);
        
        scanner.close();
    }

    public static void main(String[] args) {
        StudentGradeTracker tracker = new StudentGradeTracker();
        tracker.run();
    }
}