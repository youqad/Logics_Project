module BoolMap = Map.Make(struct type t = int let compare = Pervasives.compare end)

type boolexpr =
  | Var of int
  | Or of boolexpr * boolexpr
  | And of boolexpr * boolexpr
  | Not of boolexpr

let rec evaluate expr env = (match expr with
  | Var(x) -> BoolMap.find x env
  | Not(x) -> not (evaluate x env)
  | Or(x,y) -> (evaluate x env) || (evaluate y env)
  | And(x,y) -> (evaluate x env) && (evaluate y env));;

let naive_SAT_2 expr =
  let rec create_env expr env = (match expr with
    | Var(x) -> (List.map (BoolMap.add x true) env)@(List.map (BoolMap.add x false) env)
    | Not(x) -> create_env x env
    | Or(x,y) | And(x,y) -> let env' = create_env x env in create_env y env') in
  List.fold_left (fun bool env -> bool || (evaluate expr env)) false (create_env expr [BoolMap.empty]);;

let naive_SAT expr =
  let rec number_vars expr num_vars = match expr with
      | Var(x) -> if x > num_vars then 1 else 0
      | Not(x) -> number_vars x num_vars
      | Or(x,y) | And(x,y) -> number_vars x num_vars + number_vars y num_vars in
  let num_vars = number_vars expr 0 in
  let rec test_env env = function
    | n when n < num_vars -> let env_true = test_env (BoolMap.add n true env) (n+1) in
      if fst env_true then
        env_true
      else test_env (BoolMap.add n false env) (n+1)
    | n -> let env1, env2 = BoolMap.add n true env, BoolMap.add n false env in
      if evaluate expr env1 then
        true, env1
      else
        evaluate expr env2, env2 in

test_env BoolMap.empty 1;;

let print_map key value = let skey = (string_of_int key) and sval = (string_of_bool value) in
                    print_string(skey ^ " : " ^ sval ^ "\n");;

(* evaluate (And(Or(Var("x"),Var("y")),Var("z"))) ([("x",-24);("y",-16);("z",-8)]);;
*)

let result, env = naive_SAT (And(And(Not(Var(1)),Not(Var(2))),Not(Var(3)))) in
(
  print_string (string_of_bool result);
  print_newline ();
  BoolMap.iter print_map env;
)
