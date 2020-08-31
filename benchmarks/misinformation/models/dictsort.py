

from numpy import mean

crtime = {'Fake1-pers': 1.0, 'Fake2-pers': 1.0, 'Fake3-pers': 1.0, 'Fake4-pers': 1.0, 'Fake5-pers': 1.0, 'Fake6-pers': 1.0, 'Fake7-pers': 1.0, 'Fake8-pers': 1.0, 'Fake10-pers': 1.0, 'Fake11-pers': 1.0, 'Fake12-pers': 1.0, 'Fake13-pers': 1.0, 'Fake14-pers': 1.0, 'Fake15-pers': 1.0, 'Fake16-pers': 1.0, 'Fake17-pers': 1.0, 'Fake18-pers': 1.0, 'Real1-pers': 1.0, 'Real2-pers': 1.0, 'Real3-pers': 1.0, 'Real4-pers': 1.0, 'Real5-pers': 1.0, 'Real6-pers': 1.0, 'Real7-pers': 1.0, 'Real8-pers': 1.0, 'Real9-pers': 1.0, 'Real10-pers': 1.0, 'Real11-pers': 1.0, 'Real12-pers': 1.0, 'Real13-pers': 1.0, 'Real14-pers': 1.0, 'Real15-pers': 1.0, 'Real16-pers': 1.0, 'Real17-pers': 1.0, 'Real18-pers': 1.0, 'Fake1-glob': 0.8145233831267966, 'Fake2-glob': 0.8807514279740465, 'Fake11-glob': 0.8600452293686263, 'Fake12-glob': 0.8692087373535697, 'Fake13-glob': 0.7962142034053173, 'Fake14-glob': 0.8785554252616713, 'Fake15-glob': 0.8912544554886062, 'Fake16-glob': 0.8324622070318783, 'Fake17-glob': 0.7719258340594868, 'Fake18-glob': 0.7384872983455186, 'Real1-glob': 0.5468459756416787, 'Real2-glob': 0.5790196605838467, 'Fake3-glob': 0.8653368596827944, 'Real3-glob': 0.5560432247262216, 'Real4-glob': 0.5215909820508878, 'Real5-glob': 0.6016312025711413, 'Real6-glob': 0.5148814822507243, 'Real7-glob': 0.5646045781735266, 'Real8-glob': 0.5107715632573548, 'Real9-glob': 0.6064908568859478, 'Real10-glob': 0.5635886831628248, 'Real11-glob': 0.5781714605360776, 'Real12-glob': 0.5901395494130172, 'Fake4-glob': 0.7842001768606828, 'Real13-glob': 0.5439546207573995, 'Real14-glob': 0.6118285624397907, 'Real15-glob': 0.5186416480104223, 'Real16-glob': 0.5795255558308519, 'Real17-glob': 0.5874770982004806, 'Real18-glob': 0.5311524268779302, 'Fake5-glob': 0.829052395266567, 'Fake6-glob': 0.8581204539061228, 'Fake7-glob': 0.8734834353506379, 'Fake8-glob': 0.8450656626895487, 'Fake10-glob': 0.7619557078139843}
smr =  {'Fake1-pers': 0.5, 'Fake2-pers': 1.0, 'Fake3-pers': 0.5, 'Fake4-pers': 1.0, 'Fake5-pers': 1.0, 'Fake6-pers': 1.0, 'Fake7-pers': 1.0, 'Fake8-pers': 1.0, 'Fake10-pers': 0.5, 'Fake11-pers': 1.0, 'Fake12-pers': 0.5, 'Fake13-pers': 0.5, 'Fake14-pers': 0.5, 'Fake15-pers': 1.0, 'Fake16-pers': 1.0, 'Fake17-pers': 1.0, 'Fake18-pers': 0.5, 'Real1-pers': 0.5, 'Real2-pers': 0.5, 'Real3-pers': 1.0, 'Real4-pers': 0.5, 'Real5-pers': 1.0, 'Real6-pers': 1.0, 'Real7-pers': 0.5, 'Real8-pers': 1.0, 'Real9-pers': 1.0, 'Real10-pers': 0.5, 'Real11-pers': 0.5, 'Real12-pers': 1.0, 'Real13-pers': 1.0, 'Real14-pers': 0.5, 'Real15-pers': 0.5, 'Real16-pers': 0.5, 'Real17-pers': 1.0, 'Real18-pers': 0.5, 'Fake1-glob': 0.7489130434782608, 'Fake2-glob': 0.9195652173913044, 'Fake11-glob': 0.8978260869565218, 'Fake12-glob': 0.7880434782608695, 'Fake13-glob': 0.7054347826086956, 'Fake14-glob': 0.7880434782608695, 'Fake15-glob': 0.9434782608695652, 'Fake16-glob': 0.8891304347826087, 'Fake17-glob': 0.6184782608695653, 'Fake18-glob': 0.6728260869565217, 'Real1-glob': 0.5, 'Real2-glob': 0.5, 'Fake3-glob': 0.7902173913043479, 'Real3-glob': 0.3706521739130435, 'Real4-glob': 0.5, 'Real5-glob': 0.17391304347826086, 'Real6-glob': 0.4532608695652174, 'Real7-glob': 0.5, 'Real8-glob': 0.45869565217391306, 'Real9-glob': 0.3576086956521739, 'Real10-glob': 0.5, 'Real11-glob': 0.29456521739130437, 'Real12-glob': 0.1826086956521739, 'Fake4-glob': 0.8108695652173913, 'Real13-glob': 0.33260869565217394, 'Real14-glob': 0.5, 'Real15-glob': 0.5, 'Real16-glob': 0.5, 'Real17-glob': 0.2326086956521739, 'Real18-glob': 0.35543478260869565, 'Fake5-glob': 0.8760869565217392, 'Fake6-glob': 0.6010869565217392, 'Fake7-glob': 0.941304347826087, 'Fake8-glob': 0.8847826086956522, 'Fake10-glob': 0.6967391304347826}
zig = {'Fake1-glob': 0.8478260869565217, 'Fake2-glob': 0.9195652173913044, 'Fake11-glob': 0.8978260869565218, 'Fake12-glob': 0.9173913043478261, 'Fake13-glob': 0.8304347826086956, 'Fake14-glob': 0.9217391304347826, 'Fake15-glob': 0.9434782608695652, 'Fake16-glob': 0.8891304347826087, 'Fake17-glob': 0.7956521739130434, 'Fake18-glob': 0.7630434782608696, 'Real1-glob': 0.7304347826086957, 'Real2-glob': 0.7869565217391304, 'Fake3-glob': 0.9130434782608695, 'Real3-glob': 0.7391304347826086, 'Real4-glob': 0.5804347826086956, 'Real5-glob': 0.45869565217391306, 'Real6-glob': 0.45217391304347826, 'Real7-glob': 0.7478260869565218, 'Real8-glob': 0.6347826086956522, 'Real9-glob': 0.85, 'Real10-glob': 0.6869565217391305, 'Real11-glob': 0.24347826086956523, 'Real12-glob': 0.7021739130434783, 'Fake4-glob': 0.8108695652173913, 'Real13-glob': 0.33260869565217394, 'Real14-glob': 0.8652173913043478, 'Real15-glob': 0.5739130434782609, 'Real16-glob': 0.7695652173913043, 'Real17-glob': 0.6956521739130435, 'Real18-glob': 0.358695652173913, 'Fake5-glob': 0.8760869565217392, 'Fake6-glob': 0.908695652173913, 'Fake7-glob': 0.941304347826087, 'Fake8-glob': 0.8847826086956522, 'Fake10-glob': 0.7978260869565217}
lp = {'Fake1-pers': 0, 'Fake2-pers': 0, 'Fake3-pers': 0, 'Fake4-pers': 0, 'Fake5-pers': 0, 'Fake6-pers': 0, 'Fake7-pers': 0, 'Fake8-pers': 0, 'Fake10-pers': 0, 'Fake11-pers': 0, 'Fake12-pers': 0, 'Fake13-pers': 0, 'Fake14-pers': 0, 'Fake15-pers': 0, 'Fake16-pers': 0, 'Fake17-pers': 0, 'Fake18-pers': 0, 'Real1-pers': 0, 'Real2-pers': 1.0, 'Real3-pers': 0, 'Real4-pers': 1.0, 'Real5-pers': 0, 'Real6-pers': 1.0, 'Real7-pers': 0, 'Real8-pers': 1.0, 'Real9-pers': 1.0, 'Real10-pers': 1.0, 'Real11-pers': 0, 'Real12-pers': 1.0, 'Real13-pers': 0, 'Real14-pers': 0, 'Real15-pers': 0, 'Real16-pers': 0, 'Real17-pers': 0, 'Real18-pers': 0, 'Fake1-glob': 0.8478260869565217, 'Fake2-glob': 0.9195652173913044, 'Fake11-glob': 0.8978260869565218, 'Fake12-glob': 0.9173913043478261, 'Fake13-glob': 0.8304347826086956, 'Fake14-glob': 0.9217391304347826, 'Fake15-glob': 0.9434782608695652, 'Fake16-glob': 0.8891304347826087, 'Fake17-glob': 0.7956521739130434, 'Fake18-glob': 0.7630434782608696, 'Real1-glob': 0.7304347826086957, 'Real2-glob': 0.7869565217391304, 'Fake3-glob': 0.9130434782608695, 'Real3-glob': 0.7391304347826086, 'Real4-glob': 0.5804347826086956, 'Real5-glob': 0.17391304347826086, 'Real6-glob': 0.5478260869565217, 'Real7-glob': 0.25217391304347825, 'Real8-glob': 0.5413043478260869, 'Real9-glob': 0.85, 'Real10-glob': 0.6869565217391305, 'Real11-glob': 0.24347826086956523, 'Real12-glob': 0.8173913043478261, 'Fake4-glob': 0.8108695652173913, 'Real13-glob': 0.33260869565217394, 'Real14-glob': 0.13478260869565217, 'Real15-glob': 0.4260869565217391, 'Real16-glob': 0.23043478260869565, 'Real17-glob': 0.2326086956521739, 'Real18-glob': 0.358695652173913, 'Fake5-glob': 0.8760869565217392, 'Fake6-glob': 0.908695652173913, 'Fake7-glob': 0.941304347826087, 'Fake8-glob': 0.8847826086956522, 'Fake10-glob': 0.7978260869565217}

def sortkey(stringg):
    return int(stringg.split('-')[0][4:])

outstr = ''
for key in sorted([a for a in crtime.keys()], key=sortkey):
    if 'glob' in key and 'eal' in key:
        outstr += key.split('-')[0].replace('eal','') + '&'
        for d in [crtime,zig,lp]:
            outstr += str(round(d[key],3)) + '&'
        outstr = outstr[:-1] + '\\\\ \n' 
outstr += '\\hline\n Mean&'
for d in [crtime,zig,lp]:
    outstr += str(round(mean([float(d[key]) for key in d.keys() if 'glob' in key and 'eal' in key]),3)) + '&'
outstr = outstr[:-1] + ' \n'

        

for key in sorted([a for a in crtime.keys()], key=sortkey):
    if 'glob' in key and 'ake' in key:
        outstr += key.split('-')[0].replace('ake','') + '&'
        for d in [crtime,zig,lp]:
            outstr += str(round(1-d[key],3)) + '&'
        outstr = outstr[:-1] + '\\\\ \n' 
outstr+= '\\hline\n Mean&'
for d in [crtime,zig,lp]:
    outstr += str(round(1-mean([float(d[key]) for key in d.keys() if 'glob' in key and 'ake' in key]),3)) + '&'
outstr = outstr[:-1] + ' \n'
print(outstr)



