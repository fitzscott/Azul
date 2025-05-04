function Calc-Pct4 {
param (
$numscsv
)
# Write-Output "comma-separated number string = ${numscsv}"
$nums = $numscsv.ToString().Split(",")
$tot = 0
foreach ($num in $nums) {
# Write-Output "adding number ${num} to total"
$tot += [int]$num
}
foreach ($num in $nums) {
$pct = [math]::Round([int]$num / $tot * 100,1)
Write-Output "Percent of ${num} to total (${tot}) = ${pct}%"
}
}
