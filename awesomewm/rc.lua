-- Piece of code to put in your rc.lua 
-- Dont forget you need to add it (left_layout:add(micon))
-- and to add paths in your theme.lua (theme.micon_on = /your/path/)

-- {{{ Voice commander

micon = wibox.widget.imagebox(beautiful.micon_off)
on_off = false
micon:buttons(awful.util.table.join(awful.button({ }, 1,
function () 
    on_off = not on_off
    if on_off == true then 
        io.popen("rm /home/random/Python-exp/VoiceCommander/my_pid")
        io.popen("speech2")
        micon:set_image(beautiful.micon_on)
    else
        pid = io.popen("cat /home/random/Python-exp/VoiceCommander/my_pid")
        for i in pid:lines() do 
            io.popen("kill " .. i)
        end
        micon:set_image(beautiful.micon_off)
    end
end  )))

