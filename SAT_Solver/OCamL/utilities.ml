let read_file2 filename =
let lines = ref "0 " in
let chan = open_in filename in
try
  while true; do
    let new_line = input_line chan in
      if new_line <> "" then
        let ascii_fst_chr = Char.code new_line.[0] in
          if (47 < ascii_fst_chr && ascii_fst_chr < 58) || ascii_fst_chr = 45 || ascii_fst_chr = 32 then
            lines := !lines ^ input_line chan
      done; !lines
with End_of_file ->
  close_in chan;
  !lines ;;

List.iter (function s -> (print_int (int_of_string s); print_newline()))
  (Str.split (Str.regexp "[ \t\n\r]+") "0 -41 -42   1  0\r\n");;
