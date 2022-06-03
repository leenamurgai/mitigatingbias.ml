function Link(el)
  if el.attributes["reference-type"]=="ref" and (el.attributes["reference"]:sub(1,#"eq:")=="eq:" or el.attributes["reference"]:sub(1,#"lst:")=="lst:") then
    local citations = {}
    for cit in el.attributes["reference"]:gmatch('[^,]+') do
      citations[#citations+1] = pandoc.Citation(cit, "NormalCitation")
    end
    return pandoc.Cite("", citations)
  end
end
  
function Math(el)
  if el.mathtype == "DisplayMath" then
    local label = nil
    el.text = el.text:gsub("\\label{[^}]+}", function(w) label=w:sub(8,-2); return ""; end)
    if label ~= nil then
      return pandoc.Span(el, {id=label})
    end
  end
end

function CodeBlock(b)
  if b.attributes.label == b.identifier then
	b.attributes.label = nil;
	return b;
  end
end