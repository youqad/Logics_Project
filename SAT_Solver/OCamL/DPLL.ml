module IntSet = Set.Make(struct type t = int let compare = Pervasives.compare end)

module SetsSet = Set.Make(IntSet)

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


let rec dpll_aux clauses suitable_valuation =
  let base_cases clauses suitable_valuation =
    if SetsSet.is_empty clauses then
      Some true, Some suitable_valuation
    else if SetsSet.fold (fun y x -> x || IntSet.is_empty y) clauses false then
      Some false, None
    else None, None in

  let base_cases_result = base_cases clauses suitable_valuation in
    match base_cases_result with
      | Some bool, opt_val -> bool, opt_val
      | _ -> (
    let unit_clauses = SetsSet.fold (fun y x -> if IntSet.cardinal y=1 then
                                                  IntSet.union x y
                                        else x) clauses IntSet.empty in
    let negation_unit_clauses = IntSet.fold (fun i set -> IntSet.add (-i) set)
                                            unit_clauses IntSet.empty in
    let pure_literals = SetsSet.fold IntSet.inter clauses
        (SetsSet.fold IntSet.union clauses IntSet.empty) in
    let unit_or_pure = IntSet.union pure_literals unit_clauses in
    let neg_unit_or_pure = IntSet.union pure_literals negation_unit_clauses in
    (
      if not (IntSet.is_empty (IntSet.inter unit_clauses negation_unit_clauses))
        then false, None
      else
        let new_clauses = SetsSet.fold
            (fun clause new_clauses ->
               if not (IntSet.is_empty (IntSet.inter unit_clauses clause)) then
                 new_clauses
               else
                 SetsSet.add (IntSet.diff clause neg_unit_or_pure) new_clauses) clauses SetsSet.empty in
        let new_suitable_valuation = IntSet.union suitable_valuation
            (IntSet.fold (fun l set -> if l >= 0 then
                   IntSet.add l set
                 else set) unit_or_pure IntSet.empty) in
        let new_base_cases_result = base_cases new_clauses new_suitable_valuation in
        match new_base_cases_result with
        | Some bool, opt_val -> bool, opt_val
        | _ -> (

        let next_literal = IntSet.choose (SetsSet.fold IntSet.union new_clauses IntSet.empty) in

        let pos_clauses, neg_clauses = SetsSet.fold
            (fun clause (pos_clauses, neg_clauses) ->
               if IntSet.mem next_literal clause then
                  pos_clauses, SetsSet.add (IntSet.remove next_literal clause) neg_clauses
               else if IntSet.mem (-next_literal) clause then
                  SetsSet.add (IntSet.remove (-next_literal) clause) pos_clauses, neg_clauses
               else
                  SetsSet.add clause pos_clauses, SetsSet.add clause neg_clauses
            ) new_clauses (SetsSet.empty, SetsSet.empty) in

        let pos_suitable_valuation, neg_suitable_valuation =
          if next_literal >= 0 then
            IntSet.add next_literal new_suitable_valuation, new_suitable_valuation
          else
            new_suitable_valuation, IntSet.add (-next_literal) new_suitable_valuation
        in
          let result = dpll_aux pos_clauses pos_suitable_valuation in
            if fst result then
              result
            else
              dpll_aux neg_clauses neg_suitable_valuation
    )
  )
)

let dpll clauses =
  dpll_aux clauses IntSet.empty;;

let file = "../Examples/test3.txt";;

(* print_SetsSet (read_file file);; *)

let bool, resu = dpll (read_file file) in
match resu with
| None -> print_string (string_of_bool bool); print_newline(); print_string "None";
| Some resu -> print_string (string_of_bool bool); print_newline(); print_IntSet resu;;
