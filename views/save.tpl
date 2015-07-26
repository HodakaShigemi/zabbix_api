<html>
<header>
</header>
<body>


<form method="post">
<select id = "host_id" name="host_id" onChange="this.form.submit()">
<% for host in hosts:
    if host[0] == host_id: %>
        <option value="{{ host[0] }}" selected>{{ host[1] }}</option>
        % else:
            <option value="{{ host[0] }}">{{ host[1] }}</option>
    <% end
end%>
</select>
</form>

% try:
<form method='post'>
        {{ !form.items_id}}
        {{ !form.from_time}}
        {{ !form.to_time}}
        {{ !form.save}}
</form>
    <% except TypeError:
    pass
    end %>
</body>
</html>
