// Creates a DuoView Name Statue
// David Haas
// 7/11/23

name2 = "KATE";
name1 = "HAAS";

letter_width = 10;
platform_depth = 1;

num_characters = len(name1) > len(name2) ? len(name1) : len(name2);
echo(num_characters);

// create platform
name_width = letter_width * num_characters;
color("LightSlateGray")
rotate([0,0,45])
resize([name_width*1.5,letter_width*1.5,0])
translate([0,0,-platform_depth + 0.001])
linear_extrude(platform_depth)
circle(name_width);

function round2(x,decimals=0) = round(x * 10^decimals) / 10^decimals;
function safetan(degrees) = min(max(tan(degrees),-1),1);
echo(round2(12.3257184,3));
echo(safetan(0),safetan(30),safetan(360));


module extrude_character(char_num, letter, letter_width, position,letter_space=0, extrusion_adjustment=0) {
    // TODO: the x translate adjustment must be zero for the first name, if you set it as letter_width instead it wont work. 
    translate([
        char_num*letter_width + (0 * round2(safetan(position),2)),
        char_num*letter_width + (letter_width * round2(cos(position),2)),
        0
    ])
    rotate([90,0,position])
    linear_extrude(letter_width + extrusion_adjustment) {
        text(
            letter, 
            letter_width,
            font="Consolas:style=Regular",
            halign="center",
            spacing=0,
            valign="bottom"
        );
    };
    echo(letter,"cos(position) =", round2(cos(position),2));
    echo(letter,"sin(position) =", round2(sin(position),2));
    echo(letter,"tan(position) =", safetan(position));
}

// create the letters
translate([-name_width/2,-name_width/2,0])
for (i = [0:num_characters]) {
    intersection() {
        if (i < len(name2)) {
            extrude_character(i, name2[i],letter_width, 0);
        }
        
        if (i < len(name1)) {
            extrude_character(i, name1[i],letter_width, 90);
            
        }
    
    }
 
}
