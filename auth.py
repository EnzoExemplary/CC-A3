from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, flash

auth = Blueprint('auth', __name__, template_folder='templates')