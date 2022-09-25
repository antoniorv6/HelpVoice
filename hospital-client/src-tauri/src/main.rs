#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

use std::collections::BTreeMap;
use std::thread;
use amiquip::{Connection, ConsumerMessage, ConsumerOptions, QueueDeclareOptions, Result, ExchangeType, ExchangeDeclareOptions};
use tauri::{Manager, App, Window};

fn rbmq_connect(mut connection:Connection, window: Window) -> Result<()> {
    // Open connection.

    // Open a channel - None says let the library choose the channel ID.

    // Declare the "hello" queue.
    thread::spawn(move || -> Result<()> {
        let channel = connection.open_channel(None)?;
        println!("Starting declaring things");
        let exchange = channel.exchange_declare(ExchangeType::Direct, "hospitals", ExchangeDeclareOptions::default());
        println!("Exchange declared");
        let queue = channel.queue_declare("", QueueDeclareOptions::default())?;
        channel.queue_bind(queue.name(), "hospitals", "hospital1", BTreeMap::new());
//
        //// Start a consumer.
        let consumer = queue.consume(ConsumerOptions::default())?;
        println!("Waiting for messages. Press Ctrl-C to exit.");
        for (i, message) in consumer.receiver().iter().enumerate() {
            match message {
                ConsumerMessage::Delivery(delivery) => {
                    let body = String::from_utf8_lossy(&delivery.body);
                    println!("({:>3}) Received [{}]", i, body);
                    window.emit("new_alert", body);
                    consumer.ack(delivery)?;
                }
                other => {
                    println!("Consumer ended: {:?}", other);
                    break;
                }
            }
        }

        Ok(())
    });

    Ok(())

}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let mut connection = Connection::insecure_open("amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto");
            
            let res = match connection {
                    Ok(connection) => rbmq_connect(connection, app.get_window("main").unwrap()),
                    Err(error) => panic!("Problem opening the file: {:?}", error)
             };

             Ok(())

        })
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
