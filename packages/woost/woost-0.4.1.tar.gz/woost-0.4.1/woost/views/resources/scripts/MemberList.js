/*-----------------------------------------------------------------------------


@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			August 2009
-----------------------------------------------------------------------------*/

cocktail.init(function (root) {

    jQuery(".MemberList", root).each(function () {

        var members = [];
        var selectedMembers = [];
        var name = jQuery("input", this).get(0).name;

        jQuery(".content_type", this).each(function () {
            var prefix = jQuery(this).children(".label").text() + ": ";
            jQuery(this).children(".members").find("div").each(function () {
                var input = jQuery("input", this).get(0);
                var option = {
                    label: "<span class='content_type'>" + prefix + "</span>"
                         + "<span class='member'>" + jQuery(this).text() + "</span>",
                    value: input.value
                };
                members.push(option);
                if (input.checked) {
                    selectedMembers.push(option);
                }
            });
        });

        var memberList = document.createElement("ul");
        memberList.className = "MemberList-selection";
        jQuery(this).replaceWith(memberList);

        var inputBox = document.createElement("input");
        inputBox.type = "text";
        jQuery(memberList).after(inputBox);

        cocktail.autocomplete(inputBox, {
            options: members
        });

        jQuery(inputBox)
            .addClass("MemberList-autocomplete")
            .bind("optionSelected", function (e, option) {
                this.value = "";
                selectMember(option);
            });

        function selectMember(option) {
            var entry = document.createElement("li");
            entry.innerHTML = option.label;

            var removeButton = document.createElement("img");
            removeButton.className = "remove_button";
            removeButton.src = "/resources/images/delete_small.png";
            jQuery(removeButton).click(function () { memberList.removeChild(entry); });
            entry.appendChild(removeButton);

            var input = document.createElement("input");
            input.type = "hidden";
            input.name = name;
            input.value = option.value;
            entry.appendChild(input);

            memberList.appendChild(entry);
        }

        for (var i = 0; i < selectedMembers.length; i++) {
            selectMember(selectedMembers[i]);
        }
    });
});

