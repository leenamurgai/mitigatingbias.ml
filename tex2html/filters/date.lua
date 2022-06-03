function Meta(m)
  if m.date == "" then
    m.date = os.date("%e %B %Y")
    return m
  end
end