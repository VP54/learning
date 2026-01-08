// fn main() {
//     let mut x = 5;
//     println!("The value of x is: {x}");
//     x = 6;
//     println!("The value of x is: {x}");
// }


// SHADOWING

// fn main() {
//     let x = 5;

//     let x = x + 1;

//     {
//         let x = x * 2;
//         println!("The value of x in the inner scope is: {x}");
//     }

//     println!("The value of x is: {x}");
// }

fn before() {
    println!("This is another function before main().");
}


fn main() {
    let spaces = "   ";
    let spaces = spaces.len();

    before();
    println!("The number of spaces is: {spaces}");

    another();
}


fn another() {
    println!("This is another function.");
}