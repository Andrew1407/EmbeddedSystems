package com.diches.embeddedsystems

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val y = findViewById<EditText>(R.id.yInput)
        val population = findViewById<EditText>(R.id.popInput)
        val a = findViewById<EditText>(R.id.aInput)
        val b = findViewById<EditText>(R.id.bInput)
        val c = findViewById<EditText>(R.id.cInput)
        val d = findViewById<EditText>(R.id.dInput)

        val x1 = findViewById<TextView>(R.id.x1)
        val x2 = findViewById<TextView>(R.id.x2)
        val x3 = findViewById<TextView>(R.id.x3)
        val x4 = findViewById<TextView>(R.id.x4)

        val errField = findViewById<TextView>(R.id.errorField)
        val calcTime = findViewById<TextView>(R.id.calcTime)
        val calcBtn = findViewById<Button>(R.id.calculateBtn)

        InputHandler(calcBtn)
                .setContext(applicationContext)
                .setCoefs(listOf(a, b, c, d))
                .setResults(listOf(x1, x2, x3, x4))
                .setPopulationParams(Pair(y, population))
                .setTimeField(calcTime)
                .setErrorField(errField)
    }
}