#Had to be done in Julia due to bug #22613 of Pandas.

using CSV
using DataFrames
using DataFramesMeta
# using Plots
using LinearAlgebra
using StatsPlots
using StatsBase
gr(tickfontsize=11, labelfontsize=12)
##

results_path="./Classifications"
figures_path="./Figures"


df_ENet = DataFrame(CSV.File(joinpath(results_path,"allcandidatesandfilenames.csv"))) #Load EfficientNet candidates.
##
decode(str) = split(str,"'")[2]*".fits" #Function to have the names in the same format as in the other catalogue.
df = DataFrame(CSV.File(joinpath(results_path,"classified_0.csv")))
for i in 1:3
    append!(df, DataFrame(CSV.File(joinpath(results_path,"classified_"*string(i)*".csv"))))
end
map!(decode,df.name, df.name)
## #Matching the dataframes.
df_joined = innerjoin(df_ENet, df, on = :name)
df_disjointed = antijoin(df,df_ENet,on = :name)
df_disjointed1 = antijoin(df_ENet,df,on = :name)
## #Exporting the names of the missing images.
open(joinpath("Outputs","missed_candidates.txt"), "w") do file
    for name in df_disjointed1.name
        write(file, name*"\n")
    end
end
## Exporting the candidates (score > 0.9)
df_DeepLens_candidates = df[df.classification .> 0.9,:]
df_candidates_09 = antijoin(df_DeepLens_candidates,df_ENet,on = :name)
innerjoin(df_ENet,df_DeepLens_candidates,on = :name)
##
open(joinpath("Outputs","new_candidates.txt"), "w") do file
    for name in df_candidates_09.name
        write(file, name*"\n")
    end
end
##
@df df_joined scatter(:score, :classification,legend = false)
title!("CMUDeepLens score vs EfficientNet score")
xlabel!("EfficientNet score")
ylabel!("CMUDeepLens score")
png(joinpath(figures_path,"scatter_comparison.png"))
##

# @df df_joined marginalhist(:score, :classification)
@df df_joined marginalkde(:score, :classification,
 xlabel="EfficientNet score", ylabel="CMUDeepLens score")
png(joinpath(figures_path,"marginal_comparison.png"))
##
# histogram(df.classification, bins = :10,
#  yaxis=:log10, normalization=:probability )

hi1 = fit(Histogram, df.classification, nbins = 10, closed=:right)
hi1 = normalize(hi1,mode=:pdf)

hi2 = fit(Histogram, df_ENet.score, nbins = :10, closed=:left)
hi2 = normalize(hi2,mode=:pdf)
##

##
groupedbar( [hi1.weights hi2.weights],
    label = ["CMUDeepLens" "EfficientNet"],
    bar_position = :dodge, bar_width=0.7,
    yaxis=(:log10), xticks=(1:1:10, 0.0:0.1:1),
    # xticks = string.(0.1:0.1:1),
    ylims = (10^-2.4,10.1),
    yticks = 10 .^ (-4.0:1:1),
    plot_title = "Scores: CMUDeepLens vs EfficientNet",
    xlabel = "Score", ylabel = "Density"
    )
png(joinpath(figures_path,"histograms.png"))