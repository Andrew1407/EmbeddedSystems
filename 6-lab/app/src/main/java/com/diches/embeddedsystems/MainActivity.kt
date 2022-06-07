package com.diches.embeddedsystems

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.*
import com.diches.embeddedsystems.perceptron.Perceptron

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val calcBtn = findViewById<Button>(R.id.calculateBtn)
        val thresholdInput = findViewById<EditText>(R.id.thresholdInput)
        val iterationsRadio = findViewById<RadioButton>(R.id.iterationsDeadline)
        val timeRadio = findViewById<RadioButton>(R.id.timeDeadline)

        val firstWeightOutput = findViewById<TextView>(R.id.weights1Output)
        val secondWeightOutput = findViewById<TextView>(R.id.weights2Output)
        val timeElapsed = findViewById<TextView>(R.id.calcTime)
        val iterationsOutput = findViewById<TextView>(R.id.iterationsOutput)

        val learningRateSpinner = findViewById<Spinner>(R.id.learningRateSpinner)
        val timeDeadlineSpinner = findViewById<Spinner>(R.id.timeDeadlineSpinner)
        val iterationsDeadlineSpinner = findViewById<Spinner>(R.id.iterationsDeadlineSpinner)
        addSpinnerAdapter(learningRateSpinner, R.array.learning_rates)
        addSpinnerAdapter(timeDeadlineSpinner, R.array.time_deadline)
        addSpinnerAdapter(iterationsDeadlineSpinner, R.array.iterations_deadline)

        InputHandler(calcBtn, thresholdInput)
                .handleLearningRateSelected(learningRateSpinner)
                .handleTimeDeadlineSelected(timeDeadlineSpinner)
                .handleIterationsDeadlineSelected(iterationsDeadlineSpinner)
                .handleRadioButtonsSelected(listOf(timeRadio, iterationsRadio))
                .handleOutputs(firstWeightOutput, secondWeightOutput, timeElapsed, iterationsOutput)
    }

    private fun addSpinnerAdapter(spinner: Spinner, arrayRes: Int) {
        ArrayAdapter
                .createFromResource(this, arrayRes, android.R.layout.simple_spinner_item)
                .also {
                    it.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
                    spinner.adapter = it
                }
    }

}