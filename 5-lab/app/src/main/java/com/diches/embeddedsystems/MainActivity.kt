package com.diches.embeddedsystems

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val calculateBtn = findViewById<Button>(R.id.calculateBtn)
        val fieldA = findViewById<TextView>(R.id.firstNumber)
        val fieldB = findViewById<TextView>(R.id.secondNumber)
        val errorField = findViewById<TextView>(R.id.inputError)
        val input = findViewById<EditText>(R.id.numberInput)

        InputHandler(calculateBtn)
                .setContext(this)
                .setInput(input)
                .setResultFields(fieldA, fieldB)
                .setErrorField(errorField)
    }
}