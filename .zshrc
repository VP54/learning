export WORK=~/Desktop/programming/work
export PERSONAL=~/Desktop/programming/personal
export RESEARCH=~/Desktop/programming/personal/quant_research

export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH
export PYSPARK_PYTHON=/opt/homebrew/bin/python3.11
export PYSPARK_DRIVER_PYTHON=/opt/homebrew/bin/python3.11
export SPARK_HOME=/opt/spark-3.4.3-bin-hadoop3
export PATH=$SPARK_HOME/bin:$PATH

export SPARK_LOCAL_IP="127.0.0.1"
export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"

gs() {
	git status
	return 1
}

gcp() {
  branch=$(git rev-parse --abbrev-ref HEAD)
  git add .
  git commit -m "wip"
  git push origin "$branch"
  open -a "Google Chrome" "$repo_url/compare/$branch?expand=1"
}


gcpm() {
  echo -n "Enter commit message: "
  read message
  if [[ -z "$message" ]]; then
    echo "Aborting commit due to empty message."
    return 1
  fi
  branch=$(git rev-parse --abbrev-ref HEAD)
  git add .
  git commit -m "$message"
  git push origin "$branch"
  open -a "Google Chrome" "$repo_url/compare/$branch?expand=1"
}

gbd() {
    echo -n "Enter branch to delete: "
    read branch

    if [[ -z "$branch" ]]; then
        echo "No branch name entered."
        return 1
    fi

    if ! git show-ref --verify --quiet "refs/heads/$branch"; then
        echo "Branch '$branch' does not exist."
        return 1
    fi

}


gcb() {
    echo -n "Enter new branch name: "
    read branch
    git checkout -b "$branch"
}


gp() {
  local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  local repo_url=$(git remote get-url origin | sed -E 's#(git@|https://)#https://#; s#github.com:#github.com/#; s#\.git$##')

  if [[ -z "$branch" ]]; then
    echo "❌ Not inside a Git repository."
    return 1
  fi

  git push origin "$branch" || return 1

  open -a "Google Chrome" "$repo_url/compare/$branch?expand=1"
}

gcm() {
	echo -n "Enter commit message: "
	read message
	git commit -m "$message"
}

# Load version control information
autoload -Uz vcs_info
precmd() { vcs_info }

# Format the vcs_info_msg_0_ variable
zstyle ':vcs_info:git:*' formats '%b'

# Set up the prompt (with git branch name)
setopt PROMPT_SUBST

PROMPT='[%n@%m %1~]%F{green}(${vcs_info_msg_0_})%F{white}$ '