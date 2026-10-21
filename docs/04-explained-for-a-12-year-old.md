# Recovery Phrase Shortener, Explained for a 12-Year-Old

## What is a crypto wallet?

Think of a crypto wallet like a locked treasure chest. The key to the chest is a secret. In NEAR, the key is written as 12 ordinary words, called a recovery phrase. If you have the 12 words, you can open the chest. If someone else gets them, they can take everything inside.

## The problem

Twelve words are long. You have to write them down, keep them safe, and type them perfectly. People lose the paper, make typing mistakes, or take a photo that someone else can see.

## What our app does

Our app makes a shorter list of words from your 12 words. It is like writing your treasure code on a smaller card. But a small card cannot hold everything by itself, so you also use a secret you remember, like a special sentence only you know.

- The short card alone is not enough to open the chest.
- The short card plus your secret brings back the original 12 words.
- Then the chest opens, exactly the same as before.

## How it works, step by step

1. You type your 12 words into the app.
2. You make up a long secret sentence.
3. The app mixes your words and your secret together and shows you a short card.
4. Later, you type the short card and your secret, and the app brings back the 12 words.
5. We test it by putting a small amount of pretend money in the chest and sending it, to prove the chest opens.

## Why it works offline

The app does its math on your own device. It never sends your words or your secret anywhere. Nobody else can see them.

## What could go wrong?

- If you forget your secret, the short card is useless. Keep the secret safe, just as you would keep the 12 words safe.
- If your secret is very easy, like "1234", a clever person could try lots of guesses. So the app asks for a long, hard-to-guess secret.
- This is a school-style prototype, not a bank. Do not put real treasure in it yet.

## How it is built

- The app uses a standard word list (the same one many wallets use) to turn numbers into words.
- It uses a known math recipe to turn the 12 words into a key for the NEAR chest.
- It has a checker that tests the whole process with thousands of random examples.
- It has a small web page or script that you can run on your computer.

## One sentence to remember

The short card keeps your treasure safe, and your secret is the other half of the lock.
