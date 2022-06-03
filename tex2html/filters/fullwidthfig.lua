-- See https://groups.google.com/g/pandoc-discuss/c/NYS6FfbOhO0

function Para(el)
    if (#el.c == 1 and el.c[1].t == "Image" and el.c[1].identifier=="fig:Taxonomy") then
        --print "found"
        el.classes[1] = "fullwidth"
        return el
    end
end

function Image(el)
    if el.identifier == "fig:Taxonomy" then
        --print ("found", el.classes[1])
        el.classes[1] = "fullwidth"
        --print (el.classes[1])
        return el
    end
end