<html>
<header>
</header>
<body>
{{ !form.host_id.label}}
<form method='post'>
    {{ !form.host_id(onChange='this.form.submit()')}}
</form>
<form>
    %try:
        {{ !form.items_id}}
        {{ !form.save}}
    <% except TypeError:
    pass
    end %>
</body>
</html>