package com.diches.embeddedsystems

import android.content.Context
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast

class InputHandler(submitter: Button) {
    private lateinit var fieldA: TextView
    private lateinit var fieldB: TextView
    private lateinit var errorField: TextView
    private lateinit var inputField: EditText
    private lateinit var ctx: Context

    init {
        submitter.setOnClickListener {
            submitOnClick()
        }
    }

    fun setContext(context: Context): InputHandler {
        ctx = context
        return this
    }

    fun setResultFields(a: TextView, b: TextView): InputHandler {
        fieldA = a
        fieldB = b
        return this
    }

    fun setErrorField(err: TextView): InputHandler {
        errorField = err
        return this
    }

    fun setInput(input: EditText): InputHandler {
        inputField = input
        return this
    }

    private fun submitOnClick() {
        val inputStr = inputField.text.toString()
        if (!isNumber(inputStr)) {
            cleanResults()
            return
        }
        val (resTime, res) = FermaFunction(inputStr.toLong())
        val (a, b) = res
        showTime(resTime)
        when {
            a == 0L && b == 0L -> {
                errorField.text = InputErrors.IS_EVEN.msg
                cleanResults()
            }
            a == -1L && b == -1L -> {
                errorField.text = InputErrors.NOT_FACTORIZED.msg
                cleanResults()
            }
            a == -2L && b == -2L -> {
                errorField.text = InputErrors.OUT_OF_TIME.msg
                cleanResults()
            }
            else -> {
                fieldA.text = "a = $a"
                fieldB.text = "b = $b"
                errorField.text = ""
            }
        }
    }

    private fun isNumber(str: String): Boolean = when {
        str.isEmpty() -> {
            errorField.text = InputErrors.IS_EMPTY.msg
            false
        }
        !Regex("""\d+""").matches(str) -> {
            errorField.text = InputErrors.NOT_INT.msg
            false
        }
        else -> {
            errorField.text = ""
            true
        }
    }

    private fun showTime(timeMs: Long) {
        val msg = "Time elapsed: $timeMs ms."
        Toast.makeText(ctx, msg, Toast.LENGTH_SHORT).show()
    }

    private fun cleanResults() {
        fieldA.text = ""
        fieldB.text = ""
    }
}