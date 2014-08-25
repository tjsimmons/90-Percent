$(document).ready(function() {
    $(".edit").click(function() {
        var $parent = $(this).parents(".panel");
        var $editables = $parent.find(".editable");
        var $buttons = $parent.find(".cancel, .save");

        $editables.each(function(index) {
            var text = $(this).text();

            $(this).html("<input type='text' class='form-control' value='" + text + "'>");
        });


        $buttons.show();
        $(this).hide();
    });

    $(".cancel, .save").click(function() {
        var $parent = $(this).parents(".panel");
        var $editables = $parent.find(".editable");
        var $buttons = $parent.find(".cancel, .save");
        var $edit = $parent.find(".edit");

        $(".editable").each(function(index) {
            var value = $(this).children("input").val();

            $(this).html("");
            $(this).text(value);
        });

        $edit.show();
        $buttons.hide();
    });
});
