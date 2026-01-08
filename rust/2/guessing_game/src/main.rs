use std::cmp::Ordering;
use std::io;
use rand::Rng;


fn main() {

    let secret_number = rand::rng().random_range(1..=100);

    loop {
        println!("Guess the number!");
        let mut guess = String::new();

        io::stdin().read_line(&mut guess).expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };


        println!("You guessed: {guess} correct number was {secret_number}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }

}
