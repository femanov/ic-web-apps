CREATE OR REPLACE FUNCTION public.calc_mode_type(
	mode_id integer)
    RETURNS jsonb
    LANGUAGE 'plpython3u'
    TRANSFORM FOR TYPE jsonb
    COST 100
    STABLE
AS $BODY$
mode_plan = SD.get("mode_plan", plpy.prepare("select data->'data' as data from mode where id=$1", ['integer']) )
SD["mag_cur_plan"] = mode_plan
try:
    mode_data = plpy.execute(mode_plan, [mode_id])[0]['data']
    #return mode_data
except:
    return 'None'
chans = {
'3m4n5.Iset':None,
'5M1t4.Iset':None,
'6M1t4.Iset':None,
}

for c in chans:
    ids = plpy.execute("select id from fullchan where chan_name like \'%" + c + "\'")
    for x in ids:
        if str(x['id']) in mode_data:
            chans[c] = mode_data[str(x['id'])][0]
            break
#return chans

if chans['3m4n5.Iset'] == 0 and chans['5M1t4.Iset'] > 820 and chans['6M1t4.Iset'] > 820:
    return 'p2v2'
elif chans['3m4n5.Iset'] == 0 and chans['5M1t4.Iset'] > 820 and and chans['6M1t4.Iset'] == 0:
    return 'p2v4'
elif chans['3m4n5.Iset'] > 250 and chans['5M1t4.Iset'] < -820 and and chans['6M1t4.Iset'] == 0:
    return 'e2v4'
elif chans['3m4n5.Iset'] > 250 and chans['5M1t4.Iset'] < -820 and and chans['6M1t4.Iset'] < -820:
    return 'e2v2'
return 'None'

$BODY$;

ALTER FUNCTION public.calc_mode_type(integer)
    OWNER TO postgres;
