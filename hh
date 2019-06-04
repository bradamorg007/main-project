public class practise {

//
    static public String function(String input){

        // Remove All characters that are not numbers between 0 and 9.

         input = input.replaceAll("[^0-9]","");

         if (input.isBlank() || input.isEmpty()) {

            throw new IllegalArgumentException("The input String must contain 1 or more integer values");

         }else{

             // create an empty ArrayList to store (partial) permutations
             List<String> buffer = new ArrayList<>();

             // initialize the list with the first character of the string
             buffer.add(String.valueOf(input.charAt(0)));

             // do for every character of the specified string
             for (int i = 1; i < input.length(); i++)
             {
                 // consider previously constructed partial permutation one by one

                 // iterate backwards to skipping element when removing elements within a loop
                 for (int j = buffer.size() - 1; j >= 0 ; j--)
                 {
                     String str = buffer.remove(j);

                     // input next character of the specified string in all
                     // possible positions of current partial permutation. Then
                     // insert each of these newly constructed string in the list

                     for (int k = 0; k <= str.length(); k++)
                     {
                         // concatenate strings
                         buffer.add(str.substring(0, k) + input.charAt(i) +
                                 str.substring(k));
                     }
                 }
             }

             // sort the array then reverse the order to get largest permutations first
             Collections.sort(buffer, Collections.reverseOrder());
             return buffer.toString();

         }
    }



    static public void main(String args[]){

        String a = "A 3B2 C6D7";
        String h = function(a);
        System.out.println(h);

    }


}
