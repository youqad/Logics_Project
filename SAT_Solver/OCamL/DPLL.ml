module IntSet = Set.Make(struct type t = int let compare = Pervasives.compare end)

module SetsSet = Set.Make(IntSet)

let file = "../Examples/test.txt"

let read_file filename =
let clauses = ref SetsSet.empty in
let current_IntSet = ref IntSet.empty in
let chan = open_in filename in
try
  while true; do
    let new_line = input_line chan in
      if new_line <> "" then
        let ascii_fst_chr = Char.code new_line.[0] in
          if (47 < ascii_fst_chr && ascii_fst_chr < 58) || ascii_fst_chr = 45 || ascii_fst_chr = 32 then
            let list_numbers = List.map int_of_string
                (Str.split (Str.regexp "[ \t\n\r]+") new_line) in (
              List.iter (function
                  | 0 -> (clauses := SetsSet.add (!current_IntSet) (!clauses); current_IntSet := IntSet.empty)
                  | i -> (current_IntSet := IntSet.add i (!current_IntSet))
                ) list_numbers
            )
      done; !clauses
with End_of_file ->
  close_in chan;
  !clauses ;;

let print_IntSet s = (
  print_string "{ ";
  IntSet.iter (function i -> print_int i; print_string " || ") s;
  print_string "} ";
)

let print_SetsSet s =
  SetsSet.iter (function set -> print_IntSet set; print_newline()) s;;


print_SetsSet (read_file file);;

let evaluate clauses valuation =
  let evaluate_clause c =
    IntSet.fold (fun y x -> x || let is_y_in_val = IntSet.mem (abs y) valuation in
                  if y >= 0 then is_y_in_val else not is_y_in_val
                )
            c false in
  SetsSet.fold (fun y x -> x && evaluate_clause y) clauses true

let number_variables clauses =
  let all_literals = SetsSet.fold IntSet.union clauses IntSet.empty in
  IntSet.cardinal (IntSet.filter (function i -> i>=0) all_literals)

let naive_SAT clauses =
  let n = number_variables clauses in
  let two_pow_n = int_of_float (2.**(float_of_int n))
  and valuation = ref IntSet.empty in
  let binary_of_int number_bits = function
    | 0 -> Array.make number_bits false
    | n -> let rec aux acc = function
        | 0 -> acc
        | i -> aux ((if (i land 1) = 1 then true else false) :: acc) (i lsr 1) in
      let trunc_array = Array.of_list (aux [] n) in
      Array.append (Array.make (number_bits - Array.length trunc_array) false)
                    trunc_array in
  try
    for int_valuation = 0 to two_pow_n do
      (
        valuation := IntSet.empty;
        let binary_valuation = binary_of_int n int_valuation in
          Array.iteri (fun i bool -> match bool with
              |true -> valuation := IntSet.add (i+1) (!valuation)
              | _ -> ())
            binary_valuation;
          if evaluate clauses (!valuation) then raise Exit;
      )
     done;
     false, None
  with Exit -> true, Some (!valuation);;
