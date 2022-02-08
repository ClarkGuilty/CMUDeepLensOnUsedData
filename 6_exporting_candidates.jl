using Glob

"useless in the end."
function voccursin(files,place)
    for file in files
        if occursin(file,place)
            return true
        end
    end
end

"Inspired by stevengj from discourse.julialang."
function rdir(dir::AbstractString, pat)
    result = String[]
    i = 0.0
    initial_time = time()
    for (root, dirs, files) in walkdir(dir)
        append!(result, vfilter(pat,joinpath.(root,files)))
        i += 1
        # (i % 5000 == 0) ? println(i/4689) : 0
        if i % 50 == 0
            percentage = i/4689
            actual_time = time()
            println(100*percentage," T: ", actual_time - initial_time, 
            " TT: ", (actual_time - initial_time)/percentage )
            
        end
    end
    return result
end

"Returns a list with the filenames of the files in files which match with patterns in s."
function vfilter(files, s)
    result = []
    for file in files
        append!(result,filter(f -> occursin(file, f),s))
    end
    result
end
##
data_path="./Data"
initial_path = "CFIS_real"
final_path = "Extracted_candidates"
outputs_path = "Outputs"
candidates_file = "new_candidates.txt"
##
files_to_search = readlines(joinpath(outputs_path,candidates_file))
##
list_of_new_candidates = rdir(joinpath(data_path,initial_path),files_to_search)

open(joinpath("Outputs","new_candidates_fullPath.txt"), "w") do file
    for name in list_of_new_candidates
        write(file, name*"\n")
    end
end

## Verification. I found more files after selection.
backup = copy(list_of_new_candidates)

decode(str) = split(str,"/")[6] #Function to have the names in the same format as in the other catalogue.
df_list_exported = DataFrame()
df_list_exported.name = map(decode,list_of_new_candidates)
df_list_original = DataFrame()
df_list_original.name = files_to_search

# df_joined = innerjoin(df_list_original, df_list_exported, on = :name)
size(antijoin(df_list_original, df_list_exported,on = :name))[1] == 0 ? 
    println("No candidate is missing.") : println("There are "*string(size(antijoin(df_list_original, df_list_exported,on = :name))[1])*" missing candidates")
size(antijoin(df_list_exported,df_list_original,on = :name))[1] == 0 ? 
    println("There are no false candidates.") : println("There are "*string(size(antijoin(df_list_exported,df_list_original,on = :name))[1])*" false candidates")



