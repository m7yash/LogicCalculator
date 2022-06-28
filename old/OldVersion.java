import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class OldVersion {
    public static void main(String[] args) {
        while (true) {
            generateTable();
        }
    }

    public static String[][] generateTable() {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter proposition names (each should be one character). Separate each with a single space.");
        String[] propositions = sc.nextLine().split(" ");
        if (propositions[0].isBlank()) {
            System.out.println("You must have at least one proposition. Please try again");
            return new String[0][0];
        }
        Map<String, Integer> positions = new HashMap<>();
        System.out.println("Enter other propositions to calculate. Separate each with a single space. Use '!' for " +
                "negation, '&' for 'and', '|' for 'or', '#' for exclusive or, '->' for implication, or '<-> for " +
                "biconditional.");
        System.out.println("Each expression must have one operator (and therefore an operand right before and after, " +
                "like p->q). However, for using the negation, use only one operator after the '!' (like !p)");
        System.out.println("If you would like to have one of the variables be a previous computed expression, then use " +
                "its column number in the overall table.");
        System.out.println("For example, let's say your proposition names were p q r. Let's say your first computation " +
                "request is p&q, your second computation request is q#r, your third request is q&p, and your fourth is" +
                " q|r.");
        System.out.println("To do (p&q)|r as your next computation request, enter 4|r. To do (q#r)|(q&p), enter 5|6." +
                " To do ((p&q)|r)&((q#r)|(q&p)) do 8&9. Notice that in this example, these numbers all start 4 " +
                "because the first three columns of the table are taken by p q and r.");
        System.out.println("You may only enter numbers between 1 and 9");
        String[] calculatedPropositions = sc.nextLine().split(" ");
        System.out.println("How much spacing do you need for your columns (based on how complex your expressions are)" +
                "? Type 0 for low, 1 for normal, or 2 for high.");
        int spacing = sc.nextInt();
        if (spacing < 0 || spacing > 2) {
            System.out.println("Invalid input. Please try again");
            return new String[0][0];
        }
        int numRows = (int) Math.pow(2, propositions.length);
        int numCols = propositions.length + calculatedPropositions.length;
        if (calculatedPropositions[0].isBlank()) {
            numCols--;
        }
        String[][] table = new String[numRows + 1][numCols];

        for (int i = 0; i < table.length; i++) {
            for (int j = 0; j < table[i].length; j++) {
                if (i == 0) {
                    if (j < propositions.length) {
                        table[0][j] = propositions[j];
                    } else {
                        table[0][j] = calculatedPropositions[j - propositions.length];
                    }
                    positions.put(table[0][j], j);
                } else {
                    if (j < propositions.length) {
                        table[i][j] = "T";
                    } else {
                        table[i][j] = "X";
                    }
                }
            }
        }
        int toggleFrequency = numRows / 2;
        for (int j = 0; j < propositions.length; j++) {
            int i = 1;
            while (i < table.length) {
                if (table[i][j].equals("T")) {
                    i += toggleFrequency;
                }
                for (int k = 0; k < toggleFrequency; k++) {
                    table[i][j] = "F";
                    i++;
                }
            }
            toggleFrequency /= 2;
        }

        for (int j = propositions.length; j < numCols; j++) {
            String expression = table[0][j];
            String leftTerm = expression.substring(0, 1);
            int leftInteger = convertToInteger(leftTerm);
            if (leftInteger != -1) {
                leftTerm = table[0][leftInteger - 1];
            }
            String rightTerm = expression.substring(expression.length() - 1);
            int rightInteger = convertToInteger(rightTerm);
            if (rightInteger != -1) {
                rightTerm = table[0][rightInteger - 1];
            }
            for (int i = 1; i < table.length; i++) {
                if (expression.contains("!")) {
                    if (table[i][positions.get(rightTerm)].equals("T")) {
                        table[i][j] = "F";
                    } else {
                        table[i][j] = "T";
                    }
                } else if (expression.contains("&")) {
                    if ((table[i][positions.get(leftTerm)].equals("T")) && (table[i][positions.get(rightTerm)].equals("T"))) {
                        table[i][j] = "T";
                    } else {
                        table[i][j] = "F";
                    }
                } else if (expression.contains("|")) {
                    if ((table[i][positions.get(leftTerm)].equals("T")) || (table[i][positions.get(rightTerm)].equals("T"))) {
                        table[i][j] = "T";
                    } else {
                        table[i][j] = "F";
                    }
                } else if (expression.contains("#")) {
                    if (!(table[i][positions.get(leftTerm)].equals(table[i][positions.get(rightTerm)]))) {
                        table[i][j] = "T";
                    } else {
                        table[i][j] = "F";
                    }
                } else if (expression.contains("<->")) {
                    if (table[i][positions.get(leftTerm)].equals(table[i][positions.get(rightTerm)])) {
                        table[i][j] = "T";
                    } else {
                        table[i][j] = "F";
                    }
                } else if (expression.contains("->")) {
                    if ((table[i][positions.get(leftTerm)].equals("T")) && (table[i][positions.get(rightTerm)].equals("F"))) {
                        table[i][j] = "F";
                    } else {
                        table[i][j] = "T";
                    }
                } else {
                    System.out.println("Something was wrong with your input. Please try again.");
                    return new String[0][0];
                }
            }
        }

        for (int i = 0; i < table.length; i++) {
            for (int j = 0; j < table[i].length; j++) {
                if (i == 0) {
                    int potentialLeft = convertToInteger(table[i][j].substring(0, 1));
                    int potentialRight = convertToInteger(table[i][j].substring(table[i][j].length() - 1));
                    if (potentialLeft != -1) {
                        table[0][j] = "(" + table[0][potentialLeft - 1] + ")" + table[0][j].substring(1);
                        ;
                    }
                    if (potentialRight != -1) {
                        table[0][j] = table[0][j].substring(0, table[0][j].length() - 1) + "(" + table[0][potentialRight - 1] + ")";
                    }
                }
                System.out.print(table[i][j] + " ");
                int entrySize = table[i][j].length();
                for (int k = 0; k < (5 * Math.pow(5, spacing) - entrySize); k++) {
                    System.out.print(" ");
                }
            }
            System.out.println();
        }
        return table;
    }

    public static int convertToInteger(String s) {
        int i;
        try {
            i = Integer.parseInt(s);
        } catch (Exception e) {
            return -1;
        }
        if (i < 1 || i > 9) {
            return -1;
        }
        return i;
    }
}