package com.diches.embeddedsystems

import android.view.View
import android.widget.*
import com.diches.embeddedsystems.perceptron.Perceptron

class InputHandler(submitter: Button, private val thresholdView: EditText) {
    private var isTimeDeadline: Boolean = true
    private var learningRateStr: String = "0.001"
    private var deadlineValue: String = "0.5"

    private lateinit var timeDeadlineSpinner: Spinner
    private lateinit var iterationsDeadlineSpinner: Spinner
    private lateinit var firstWeightView: TextView
    private lateinit var secondWeightView: TextView
    private lateinit var timeView: TextView
    private lateinit var iterationsView: TextView

    init {
        submitter.setOnClickListener {
            handleSubmit()
        }
    }

    fun handleLearningRateSelected(spinner: Spinner): InputHandler {
        onItemSelectedSpinnerListener(spinner) {
            learningRateStr = it
        }
        return this
    }

    fun handleTimeDeadlineSelected(spinner: Spinner): InputHandler {
        timeDeadlineSpinner = spinner
        onItemSelectedSpinnerListener(timeDeadlineSpinner) {
            deadlineValue = it
        }
        return this
    }

    fun handleIterationsDeadlineSelected(spinner: Spinner): InputHandler {
        iterationsDeadlineSpinner = spinner
        onItemSelectedSpinnerListener(iterationsDeadlineSpinner) {
            deadlineValue = it
        }
        return this
    }

    private fun onItemSelectedSpinnerListener(spinner: Spinner, onSelectedClb: (input: String) -> Unit) {
        spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onNothingSelected(parent: AdapterView<*>?) { }
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                onSelectedClb(parent?.getItemAtPosition(position).toString())
            }
        }
    }

    fun handleRadioButtonsSelected(radios: List<RadioButton>): InputHandler {
        radios.forEach {
            it.setOnClickListener { view ->
                when (view.id) {
                    R.id.iterationsDeadline -> {
                        isTimeDeadline = false
                        deadlineValue = "100"
                        iterationsDeadlineSpinner.visibility = View.VISIBLE
                        timeDeadlineSpinner.visibility = View.GONE
                    }
                    R.id.timeDeadline -> {
                        isTimeDeadline = true
                        deadlineValue = "0.5"
                        iterationsDeadlineSpinner.visibility = View.GONE
                        timeDeadlineSpinner.visibility = View.VISIBLE
                    }
                }
            }
        }

        return this
    }

    fun handleOutputs(vararg views: TextView): InputHandler {
        firstWeightView = views[0]
        secondWeightView = views[1]
        timeView = views[2]
        iterationsView = views[3]
        return this
    }

    private fun handleSubmit() {
        val thresholdDefault = 4
        val p = if (thresholdView.text.isEmpty()) thresholdDefault
            else thresholdView.text.toString().toInt()
        val learningRate = learningRateStr.toFloat()
        val perceptron = Perceptron(p, learningRate)

        val (values, timeElapsed, iterations) = if (isTimeDeadline) {
            val timeDeadline = deadlineValue.toFloat()
            perceptron.calcWeights(timeDeadline)
        } else {
            val iterationsDeadline = deadlineValue.toInt()
            perceptron.calcWeights(iterationsDeadline)
        }

        firstWeightView.text = "w1 = ${values[0]}"
        secondWeightView.text = "w2 = ${values[1]}"
        timeView.text = "Time elapsed: $timeElapsed ms."
        iterationsView.text = "Iterations: $iterations"
    }
}