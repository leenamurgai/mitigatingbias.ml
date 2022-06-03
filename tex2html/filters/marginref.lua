function Cite(el)
    --print(el.citations[1].id)
    --print(#el.content)
    --print(el.content[1].content[1].text)   
    link = pandoc.Span(el.content)
    id = el.citations[1].id
    label = pandoc.Span(pandoc.Str(el.content[1].content[1].text))
    label.classes[1] = 'marginnote'
    return {link, label}
end